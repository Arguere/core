import librosa
import numpy as np
from typing import Dict
import assemblyai as aai
from app.core.config import settings


# AssemblyAI client setup
aai.settings.api_key = settings.ASSEMBLY_AI_API_KEY
transcriber = aai.Transcriber()
config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.slam_1, )


class AudioAnalyzer:
    @staticmethod
    async def analyze_audio(audio_path: str) -> Dict[str, float]:
        try:
            # Load audio file
            y, sr = librosa.load(audio_path)
            transcript = transcriber.transcribe(audio_path, config=config)
            
            if not transcript or not transcript.text or transcript.status == "error":
                raise ValueError("Transcription failed or returned empty text.", transcript.error)
            
            transcription = transcript.text
                        
            # Calculate average confidence score as a proxy for pronunciation accuracy
            word_count = transcript.words
            confidence_scores = [word.confidence for word in word_count]
            average_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            asr_accuracy = average_confidence * 100  # Scale to 0-100
            
            # Calculate speech rate (words per minute)
            duration = librosa.get_duration(y=y, sr=sr)
            speech_rate = len(transcription.split()) / duration * 60  # Words per minute
            
            # Calculate spectral clarity
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_clarity = float(np.mean(spectral_centroids))
            
            
            return {
                "speech_rate": speech_rate,
                "duration": duration,
                "spectral_clarity": spectral_clarity,
                "asr_accuracy": asr_accuracy,
                "score": AudioAnalyzer.calculate_score(speech_rate, spectral_clarity, asr_accuracy)
            }
        except Exception as e:
            raise Exception(f"Audio analysis failed: {str(e)}")

    @staticmethod
    def calculate_score(speech_rate: float, spectral_clarity: float, asr_accuracy: float) -> float:
        # Implement scoring logic based on weights
        weights = {"speech_rate": 0.3, "spectral_clarity": 0.3, "asr_accuracy": 0.4}
        normalized_speech_rate = min(speech_rate / 200, 1.0)  # Assuming 200 wpm as max
        normalized_clarity = min(spectral_clarity / 10000, 1.0)  # Example normalization
        normalized_asr = asr_accuracy / 100  # Assuming percentage
        
        score = (
            weights["speech_rate"] * normalized_speech_rate +
            weights["spectral_clarity"] * normalized_clarity +
            weights["asr_accuracy"] * normalized_asr
        ) * 100
        
        return round(score, 2)