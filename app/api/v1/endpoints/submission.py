from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from app.core.database import get_session
from app.models.submission import Submission as SubmissionModel
from app.models.feedback import Feedback as FeedbackModel
from app.models.scenario import Scenario as ScenarioModel
from app.schemas.submission import SubmissionCreate, Submission, SubmissionWithFeedback
from app.services.audio_analysis import AudioAnalyzer
from app.services.feedback_generator import FeedbackGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
import re

router = APIRouter()

async def process_submission_async(
    submission_id: uuid.UUID,
    audio_url: str,
    scenario_id: uuid.UUID
):
    """Background task to process audio and generate feedback"""
    from app.core.database import async_session
    
    async with async_session() as session:
        try:
            # Update status to processing
            stmt = select(SubmissionModel).where(SubmissionModel.id == submission_id)
            result = await session.execute(stmt)
            submission = result.scalar_one_or_none()
            
            if not submission:
                return
                
            submission.processing_status = "processing"
            await session.commit()
            
            # Get scenario details
            scenario_stmt = select(ScenarioModel).where(ScenarioModel.id == scenario_id)
            scenario_result = await session.execute(scenario_stmt)
            scenario = scenario_result.scalar_one_or_none()
            
            if not scenario:
                submission.processing_status = "failed"
                await session.commit()
                return
            
            # Analyze audio and get transcription
            audio_analysis = await AudioAnalyzer.analyze_audio(audio_url)
            
            # Update submission with transcription and metrics
            submission.transcription = audio_analysis["transcription"]
            submission.audio_metrics = audio_analysis
            
            # Generate feedback
            feedback_content = await FeedbackGenerator.generate(
                transcription=audio_analysis["transcription"],
                scenario_context=scenario.knowledge_foundation,
                guideline=scenario.guideline,
                audio_metrics=audio_analysis
            )
            
            # Extract score from feedback if possible
            score = extract_score_from_feedback(feedback_content)
            
            # Create feedback record
            feedback = FeedbackModel(
                id=uuid.uuid4(),
                submission_id=submission_id,
                content=feedback_content,
                score=score,
                audio_metrics=audio_analysis
            )
            session.add(feedback)
            
            # Update submission status
            submission.processing_status = "completed"
            await session.commit()
            
        except Exception as e:
            # Update status to failed
            try:
                stmt = select(SubmissionModel).where(SubmissionModel.id == submission_id)
                result = await session.execute(stmt)
                submission = result.scalar_one_or_none()
                if submission:
                    submission.processing_status = "failed"
                    await session.commit()
            except:
                pass
            print(f"Error processing submission {submission_id}: {str(e)}")
            
            
def extract_score_from_feedback(feedback_content: str) -> float:
    """Extract numerical score from feedback content"""
    try:
        # Look for patterns like "TOTAL SCORE: 85/100" or "Score: 85"
        patterns = [
            r"TOTAL SCORE:\s*(\d+(?:\.\d+)?)/100",
            r"Total Score:\s*(\d+(?:\.\d+)?)/100",
            r"Overall Score:\s*(\d+(?:\.\d+)?)",
            r"Score:\s*(\d+(?:\.\d+)?)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, feedback_content, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return None
    except:
        return None

@router.post("/", response_model=Submission)
async def create_submission(
    submission_data: SubmissionCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
): 
    try:
        # Validate scenario exists
        scenario_stmt = select(ScenarioModel).where(ScenarioModel.id == submission_data.scenario_id)
        scenario_result = await session.execute(scenario_stmt)
        scenario = scenario_result.scalar_one_or_none()
        
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        # Create submission record
        new_submission = SubmissionModel(
            id=uuid.uuid4(),
            scenario_id=submission_data.scenario_id,
            processing_status="pending"
        )
        session.add(new_submission)
        await session.commit()
        await session.refresh(new_submission)
        
        # Process audio in background
        background_tasks.add_task(
            process_submission_async,
            new_submission.id,
            submission_data.audio_url,
            submission_data.scenario_id
        )
        
        return new_submission
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create submission: {str(e)}")

@router.get("/{scenario_id}", response_model=List[Submission])
async def read_submissions(
    scenario_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    stmt = select(SubmissionModel).where(SubmissionModel.scenario_id == scenario_id)
    result = await session.execute(stmt)
    return result.scalars().all()

@router.get("/detail/{submission_id}", response_model=SubmissionWithFeedback)
async def get_submission_with_feedback(
    submission_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    # Get submission
    stmt = select(SubmissionModel).where(SubmissionModel.id == submission_id)
    result = await session.execute(stmt)
    submission = result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Get feedback
    feedback_stmt = select(FeedbackModel).where(FeedbackModel.submission_id == submission_id)
    feedback_result = await session.execute(feedback_stmt)
    feedback = feedback_result.scalar_one_or_none()
    
    response_data = {
        "id": submission.id,
        "scenario_id": submission.scenario_id,
        "transcription": submission.transcription,
        "audio_metrics": submission.audio_metrics,
        "processing_status": submission.processing_status,
        "created_at": submission.created_at,
        "feedback": {
            "id": feedback.id,
            "content": feedback.content,
            "score": feedback.score,
            "audio_metrics": feedback.audio_metrics,
            "created_at": feedback.created_at
        } if feedback else None
    }
    
    return response_data