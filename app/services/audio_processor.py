import librosa
import numpy as np 
import os 

from app.models.audio_features import AudioFeatures

def analyze_audio(file_path: str) -> AudioFeatures: 
    y, sr = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    rms = float(np.mean(librosa.feature.rms(y=y))) 
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitch = float(np.mean(librosa.yin(y=y, fmin=80, fmax=400)))
    
    return AudioFeatures(
        duration_seconds=duration,
        avg_rms_energy=rms,
        estimated_tempo_bpm=tempo,
        avg_pitch_hz=pitch
    )
    
    
