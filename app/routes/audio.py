from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.audio_processor import analyze_audio
from app.schemas.audio import AudioAnalysisResponse

router = APIRouter()

@router.post("/analyze", response_model=AudioAnalysisResponse)
async def analyze_audio_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to analyze audio files.
    """
    if not file.filename.endswith(('.mp3', '.wav', '.flac')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .mp3, .wav, and .flac files are allowed.")
    
    try:
        analysis_result = await analyze_audio(file)
        return JSONResponse(content=analysis_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))