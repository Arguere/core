# Monolog Core API

AI-powered communication training platform that generates personalized guidelines and provides detailed feedback on user communication skills.

## Features

- **Scenario Management**: Create communication scenarios with AI-generated guidelines
- **Audio Processing**: Analyze audio submissions from Cloudflare R2 URLs
- **Speech Analytics**: Extract speech rate, clarity, pronunciation accuracy, and more
- **AI Feedback**: Generate detailed feedback using OpenAI GPT models
- **Real-time Processing**: Asynchronous audio processing with status tracking

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL database
- OpenAI API key
- AssemblyAI API key
- Cloudflare R2 for audio storage

### Installation

1. **Clone and setup environment:**

```bash
git clone <repository>
cd monolog-core
```

2. **Install dependencies:**

```bash
poetry install
```

3. **Activate virtual environment:**

```bash
eval $(poetry env activate)
```

4. **Environment variables:**

```bash
cp .env.example .env
# Edit .env with your API keys and database URL
```

5. **Database setup:**

```bash
# Generate migration
alembic revision --autogenerate -m "add audio features"

# Apply migrations
alembic upgrade head
```

6. **Run the application:**

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Scenarios

- `POST /api/v1/scenario/` - Create a new scenario with AI-generated guidelines
- `GET /api/v1/scenario/{user_id}` - Get all scenarios for a user

### Submissions

- `POST /api/v1/submission/` - Submit audio for analysis and feedback
- `GET /api/v1/submission/{scenario_id}` - Get all submissions for a scenario
- `GET /api/v1/submission/detail/{submission_id}` - Get detailed submission with feedback

### Status & Monitoring

- `GET /api/v1/status/submission/{submission_id}/status` - Check processing status
- `GET /api/v1/status/submissions/stats/{scenario_id}` - Get scenario statistics
- `GET /api/v1/status/health/detailed` - Detailed health check

### Feedback

- `GET /api/v1/feedback/{submission_id}` - Get feedback for a submission

## Usage Flow

1. **Create a Scenario:**

```json
POST /api/v1/scenario/
{
    "user_id": "uuid",
    "context": "You are a sales representative calling a potential client to introduce our new software solution...",
    "additional_info": {}
}
```

2. **Submit Audio:**

```json
POST /api/v1/submission/
{
    "scenario_id": "uuid",
    "audio_url": "https://your-r2-bucket.com/audio/recording.wav"
}
```

3. **Check Status:**

```bash
GET /api/v1/status/submission/{submission_id}/status
```

4. **Get Results:**

```bash
GET /api/v1/submission/detail/{submission_id}
```

## Audio Analysis Features

The system analyzes:

- **Transcription**: Full speech-to-text conversion
- **Speech Rate**: Words per minute (optimal: 140-180 WPM)
- **Pronunciation Accuracy**: Based on ASR confidence scores
- **Speech Flow**: Pause analysis and rhythm
- **Volume Consistency**: Variation in speaking volume
- **Spectral Clarity**: Audio quality metrics
- **Overall Score**: Weighted composite score

## AI Feedback Components

Feedback includes:

- **Content Analysis**: Alignment with scenario guidelines
- **Delivery Assessment**: Speech quality and presentation
- **Specific Recommendations**: Actionable improvement suggestions
- **Numerical Scoring**: Detailed breakdown across multiple dimensions

## Development

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing

```bash
# Run tests (when implemented)
poetry run pytest

# Type checking
poetry run mypy app/
```

### Docker Deployment

```bash
# Build and run
docker-compose up --build

# Production deployment
docker build -t monolog-core .
docker run -p 8000:8000 monolog-core
```

## Configuration

Key environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: For AI feedback generation
- `ASSEMBLYAI_API_KEY`: For audio transcription
- `CLERK_JWKS_URL` & `CLERK_ISSUER`: For authentication

## Architecture

- **FastAPI**: Modern async web framework
- **SQLAlchemy**: Database ORM with async support
- **Alembic**: Database migrations
- **AssemblyAI**: Speech-to-text processing
- **OpenAI**: AI-powered feedback generation
- **PostgreSQL**: Primary database with JSONB support
- **Background Tasks**: Async audio processing

## Monitoring

- Health checks at `/health` and `/api/v1/status/health/detailed`
- Processing status tracking for all submissions
- Audio analysis metrics storage
- Error handling with detailed logging
