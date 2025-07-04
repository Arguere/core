import librosa
import numpy as np
import soundfile as sf
from io import BytesIO
from fastapi import UploadFile
from app.models.audio_features import AudioFeatures


async def analyze_audio(file: UploadFile) -> dict:
    # Read audio bytes
    audio_bytes = await file.read()

    # Convert bytes to file-like object
    audio_stream = BytesIO(audio_bytes)

    # Use soundfile to read the audio into y, sr
    try:
        y, sr = sf.read(audio_stream)
    except RuntimeError as e:
        raise ValueError(f"Could not decode audio: {e}")

    if y.ndim > 1:
        y = y.mean(axis=1)  # convert to mono if stereo

    duration = librosa.get_duration(y=y, sr=sr)
    rms = float(np.mean(librosa.feature.rms(y=y)))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitch = float(np.mean(librosa.yin(y, fmin=80, fmax=400)))

    return AudioFeatures(
        duration_seconds=duration,
        avg_rms_energy=rms,
        estimated_tempo_bpm=tempo,
        avg_pitch_hz=pitch
    ).dict()
