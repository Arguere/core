# Arguere

The gym for your communication

This project provides an API to analyze audio files and extract basic speech features like pitch, tempo, energy, and duration.

## Features

- Upload WAV files and receive analysis in JSON
- Extracted features: pitch, tempo, RMS energy, duration

## Run Locally

```bash
docker build -t fastapi-audio .
docker run -p 8000:8000 fastapi-audio
```

or

```bash
fastapi dev app/main.py
```

Then visit `http://localhost:8000/docs` to access the Swagger UI.

## API Usage

POST /api/audio/analyze
Form-data:

- file: (WAV file)

Response:

```json
{
  "duration_seconds": 4.2,
  "avg_rms_energy": 0.034,
  "estimated_tempo_bpm": 124.8,
  "avg_pitch_hz": 198.6
}
```

## Requirements

- Python 3.11+
- Docker (optional but recommended)
