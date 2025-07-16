from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.config import settings
from app.models.submission import Submission
from app.schemas.submission import Submission, SubmissionCreate
from app.dependencies.auth import get_current_user
from app.services.audio_analysis import AudioAnalyzer
from app.services.feedback_generator import FeedbackGenerator
from app.models.profile import Profile
from app.models.feedback import Feedback
from app.models.scenario import Scenario
from app.models.method import Method
import os
import uuid

router = APIRouter()

@router.post("/", response_model=Submission)
async def create_submission(
    scenario_id: int,
    file: UploadFile = File(None),
    text: str = None,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    if not file and not text:
        raise HTTPException(status_code=400, detail="Either file or text must be provided")
    
    content_type = "text" if text else "audio"
    content_path = None
    transcription = text if text else ""
    
    if file:
        file_extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(settings.AUDIO_UPLOAD_DIR, filename)
        
        os.makedirs(settings.AUDIO_UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        content_path = file_path
        
 
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    method = db.query(Method).filter(Method.id == scenario.method_id).first()
    if not method: 
        raise HTTPException(status_code=404, detail="Method not found")
    
    
    submission_data = SubmissionCreate(
        scenario_id=scenario_id,
        content_type=content_type,
    )
    
    db_submission = Submission(
        **submission_data.model_dump(), 
        user_id=current_user.id
    )
    
    if content_type == "audio":
        analysis_results = await AudioAnalyzer.analyze_audio(content_path)
        db_submission.speech_rate = analysis_results["speech_rate"]
        db_submission.duration = analysis_results["duration"]
        db_submission.spectral_clarity = analysis_results["spectral_clarity"]
        db_submission.asr_accuracy = analysis_results["asr_accuracy"]
        db_submission.score = analysis_results["score"]
        transcription = analysis_results["transcription"]
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    # Generate feedback
    feedback_data = await FeedbackGenerator.generate_feedback(
        transcription, 
        framework_name = method.title,
        scenario_description = scenario.description,
    )
    db_feedback = Feedback(
        submission_id=db_submission.id,
        **feedback_data
    )
    db.add(db_feedback)
    db.commit()
    
    return db_submission, db_feedback

@router.get("/{scenario_id}", response_model=List[Submission])
def read_submissions(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    return db.query(Submission).filter(
        Submission.scenario_id == scenario_id,
        Submission.user_id == current_user.id
    ).all()