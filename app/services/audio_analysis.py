import librosa
import numpy as np
from typing import Dict
import assemblyai as aai
import aiohttp
import tempfile
import os
from app.core.config import settings

# AssemblyAI client setup
aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
transcriber = aai.Transcriber()
config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.nano,
    language_detection=True
)

class AudioAnalyzer:
    @staticmethod
    async def analyze_audio(audio_url: str) -> Dict[str, float]:
        if not audio_url:
            raise ValueError("Audio URL must be provided")
        
        try:
            # Download audio file from Cloudflare R2
            temp_audio_path = await AudioAnalyzer._download_audio(audio_url)
            
            try:
                # Load audio file for librosa analysis
                y, sr = librosa.load(temp_audio_path)
                
                # Transcribe audio using AssemblyAI
                transcript = transcriber.transcribe(temp_audio_path, config=config)
                
                if not transcript or not transcript.text or transcript.status == "error":
                    raise ValueError(f"Transcription failed: {transcript.error if transcript else 'No transcript returned'}")
                
                transcription = transcript.text
                
                # Calculate audio metrics
                metrics = AudioAnalyzer._calculate_audio_metrics(y, sr, transcript)
                
                return {
                    "transcription": transcription,
                    "speech_rate": float(metrics["speech_rate"]),
                    "duration": float(metrics["duration"]),
                    "spectral_clarity": float(metrics["spectral_clarity"]),
                    "asr_accuracy": float(metrics["asr_accuracy"]),
                    "pause_analysis": float(metrics["pause_analysis"]),
                    "volume_consistency": float(metrics["volume_consistency"]),
                    "overall_score": AudioAnalyzer._calculate_overall_score(metrics)
                }
            finally:
                # Clean up temporary file
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)
                    
        except Exception as e:
            raise Exception(f"Audio analysis failed: {str(e)}")
    
    @staticmethod
    async def _download_audio(audio_url: str) -> str:
        """Download audio file from URL to temporary file"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download audio: HTTP {response.status}")
                    
                    # Create temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                    temp_path = temp_file.name
                    
                    # Write audio data to temporary file
                    async for chunk in response.content.iter_chunked(8192):
                        temp_file.write(chunk)
                    
                    temp_file.close()
                    return temp_path
        except Exception as e:
            raise Exception(f"Failed to download audio file: {str(e)}")
    
    @staticmethod
    def _calculate_audio_metrics(y: np.ndarray, sr: int, transcript) -> Dict[str, float]:
        """Calculate various audio quality metrics"""
        
        # Duration
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Speech rate (words per minute)
        word_count = len(transcript.text.split()) if transcript.text else 0
        speech_rate = (word_count / duration) * 60 if duration > 0 else 0
        
        # ASR accuracy from confidence scores
        if hasattr(transcript, 'words') and transcript.words:
            confidence_scores = [word.confidence for word in transcript.words if hasattr(word, 'confidence')]
            asr_accuracy = (sum(confidence_scores) / len(confidence_scores)) * 100 if confidence_scores else 0
        else:
            asr_accuracy = 0
        
        # Spectral clarity
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_clarity = float(np.mean(spectral_centroids))
        
        # Pause analysis (silence detection)
        hop_length = 512
        frame_length = 2048
        energy = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        silence_threshold = np.percentile(energy, 20)  # Bottom 20% as silence
        silence_frames = np.sum(energy < silence_threshold)
        total_frames = len(energy)
        silence_ratio = silence_frames / total_frames if total_frames > 0 else 0
        pause_analysis = (1 - silence_ratio) * 100  # Higher score = less silence/better flow
        
        # Volume consistency (lower standard deviation = more consistent)
        volume_std = np.std(energy)
        volume_mean = np.mean(energy)
        volume_consistency = max(0, 100 - (volume_std / volume_mean * 100)) if volume_mean > 0 else 0
        
        return {
            "speech_rate": speech_rate,
            "duration": duration,
            "spectral_clarity": spectral_clarity,
            "asr_accuracy": asr_accuracy,
            "pause_analysis": pause_analysis,
            "volume_consistency": volume_consistency
        }
    
    @staticmethod
    def _calculate_overall_score(metrics: Dict[str, float]) -> float:
        """Calculate overall audio quality score"""
        # Normalize speech rate (optimal range: 140-180 WPM)
        speech_rate_score = 100
        if metrics["speech_rate"] < 140:
            speech_rate_score = max(0, (metrics["speech_rate"] / 140) * 100)
        elif metrics["speech_rate"] > 180:
            speech_rate_score = max(0, 100 - ((metrics["speech_rate"] - 180) / 40) * 50)
        
        # Weight different metrics
        weights = {
            "asr_accuracy": 0.3,
            "speech_rate": 0.2,
            "pause_analysis": 0.2,
            "volume_consistency": 0.15,
            "spectral_clarity": 0.15
        }
        
        # Normalize spectral clarity (typical range: 1000-4000 Hz)
        spectral_clarity_normalized = min(100, (metrics["spectral_clarity"] / 4000) * 100)
        
        overall_score = (
            weights["asr_accuracy"] * metrics["asr_accuracy"] +
            weights["speech_rate"] * speech_rate_score +
            weights["pause_analysis"] * metrics["pause_analysis"] +
            weights["volume_consistency"] * metrics["volume_consistency"] +
            weights["spectral_clarity"] * spectral_clarity_normalized
        )
        
        return round(overall_score, 2)