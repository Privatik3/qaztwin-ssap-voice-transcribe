# Qaztwin SSAP Voice Transcribe

## Docker Container Status

### Whisper Container
- **Name**: `whisper-transcribe`
- **Image**: `qaztwin-ssap-dev-whisper-transcribe`
- **Ports**: 0.0.0.0:4104->8000/tcp

## Docker Configuration

### docker-compose.yml
- **Docker project name**: qaztwin-ssap-dev 
- **Service**: whisper-transcribe
- **Network**: qaztwin-net (external)
- **Port Mapping**: ${API_PORT:-8000}:8000 (defaults to 8000)
- **Volumes**:
  - Audio directory: mounted as read-only at `/app/audio`
  - Whisper source: mounted at `/app/whisper-20250625`
- **Environment Variables**:
  - API_PORT (default: 8000)
  - AUDIO_DIR (default: /home/serhii/Public/audios)
  - MODEL_SIZE (default: tiny)
  - PYTHONPATH=/app/whisper-20250625
- **Health Check**: curl http://localhost:8000/health every 30s (inside docker net)

### Dockerfile
- **Base Image**: pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
- **System Dependencies**: curl, ffmpeg
- **Python Dependencies**: numba, tqdm, more-itertools, tiktoken, fastapi, uvicorn
- **Working Directory**: /app
- **Exposed Port**: 8000

## Environment Configuration (env.example)

```
MODEL_SIZE=tiny
AUDIO_DIR=./audio
API_PORT=8000
```

**Note**: `.env` file not present, using example configuration

## API Service (main.py)

### FastAPI Application
- **Title**: Whisper Transcription API v1.0.0
- **Model**: Whisper "tiny" (loaded on startup)

### Endpoints

#### GET /health
- Health check endpoint
- Returns: `{"message": "Whisper Transcription API is running", "status": "healthy"}`

#### POST /transcribe
- Transcribes audio files from mounted audio folder
- **Request**: `{"file_path": "relative/path/to/audio.mp3"}`
- **Response**: 
  ```json
  {
    "text": "transcribed text",
    "file_path": "relative/path/to/audio.mp3",
    "language": "detected language",
    "duration": 0.0
  }
  ```
- **Supported Formats**: .mp3, .wav, .flac, .m4a, .ogg
- **Audio Path**: Files accessed from `/app/audio/`

### Error Handling
- 404: Audio file not found
- 400: Unsupported audio format
- 500: Transcription failure

## Architecture

- Whisper source code from snapshot: `whisper-20250625/`
- Audio files are mounted read-only for security
- Model loads once at startup for efficiency
- Healthcheck ensures container reliability
- Integrated with qaztwin-net network for microservices communication

## Test Audio Files

The project root contains a sample audio file `record.mp3` for testing. To use this file:

1. Copy it to your audio directory:
   ```bash
   cp record.mp3 /home/serhii/Public/audios/
   ```
2. Use the file path `record.mp3` in your API requests

You can also place your own audio files in the audio directory.

## API Testing

### Health Check
```bash
curl http://localhost:4104/health
```

**Response:**
```json
{
  "message": "Whisper Transcription API is running",
  "status": "healthy"
}
```

### Transcription Example 1: record.mp3
```bash
curl -X POST http://localhost:4104/transcribe \
  -H "Content-Type: application/json" \
  -d '{"file_path": "record.mp3"}'
```

**Response:**
```json
{
  "text": "transcribed text here",
  "file_path": "record.mp3",
  "language": "ru",
  "duration": 0.0
}
```

### Test Results Summary
- ✅ API running on port **4104**
- ✅ Health check operational
- ✅ Transcription working with Whisper tiny model
- ✅ Language detection functional (Russian, English)
- ✅ Supports multiple formats: mp3, wav, flac, m4a, ogg

