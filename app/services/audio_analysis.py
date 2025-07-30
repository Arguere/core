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
        if not audio_path:
            raise ValueError("Audio path must be provided")
        
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
                "transcription": transcription,
                "speech_rate": speech_rate,
                "duration": duration,
                "spectral_clarity": spectral_clarity,
                "asr_accuracy": asr_accuracy,
                "score": AudioAnalyzer.calculate_score(speech_rate, spectral_clarity, asr_accuracy)
            }
        except Exception as e:
            raise Exception(f"Audio analysis failed: {str(e)}")
