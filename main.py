import os
import whisper
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Whisper Transcription API", version="1.0.0")

# Global model variable
model = None

class TranscribeRequest(BaseModel):
    file_path: str

@app.on_event("startup")
async def startup_event():
    """Load the Whisper model on startup"""
    global model
    model_size = os.getenv("MODEL_SIZE", "tiny")
    print(f"Loading Whisper model: {model_size}...")
    model = whisper.load_model(model_size)
    print("Whisper model loaded successfully!")

@app.get("/health")
async def root():
    """Health check endpoint"""
    return {"message": "Whisper Transcription API is running", "status": "healthy"}

@app.post("/transcribe")
async def transcribe_audio(request: TranscribeRequest):
    """
    Transcribe audio file from the mounted audio folder

    Args:
        request: Contains file_path relative to the audio folder

    Returns:
        dict: Contains the transcribed text
    """
    try:
        # Construct full path to audio file
        audio_path = os.path.join("/app/audio", request.file_path)

        # Check if file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail=f"Audio file not found: {request.file_path}")

        # Check if file is a supported audio format
        supported_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.ogg']
        _, ext = os.path.splitext(audio_path.lower())
        if ext not in supported_extensions:
            raise HTTPException(status_code=400, detail=f"Unsupported audio format: {ext}. Supported formats: {supported_extensions}")

        print(f"Transcribing audio file: {audio_path}")

        # Perform transcription
        result = model.transcribe(audio_path)

        return {
            "text": result["text"],
            "file_path": request.file_path,
            "language": result.get("language", "unknown"),
            "duration": result.get("duration", 0.0)
        }

    except Exception as e:
        print(f"Error transcribing {request.file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
