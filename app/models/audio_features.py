from pydantic import BaseModel

class AudioFeatures(BaseModel):
    duration_seconds: float
    avg_rms_energy: float
    estimated_tempo_bpm: float
    avg_pitch_hz: float
  