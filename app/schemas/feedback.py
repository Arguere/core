from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from typing import Dict, Any, Optional, List, Literal

class FeedbackBase(BaseModel):
    submission_id: UUID4

class Feedback(FeedbackBase):
    id: UUID4
    structured_feedback: Dict[str, Any]
    overall_performance: Optional[str] = None
    total_score: Optional[int] = None
    content_alignment_score: Optional[int] = None
    scenario_appropriateness_score: Optional[int] = None
    communication_clarity_score: Optional[int] = None
    audio_delivery_score: Optional[int] = None
    
    created_at: datetime

    class Config:
        from_attributes = True

# --------- Generated feedback schema for structured evaluation
class GuidelineAdherence(BaseModel):
    score: int = Field(..., ge=0, le=25, description="Content alignment score (0-25)")
    analysis: str = Field(..., min_length=10, description="Detailed evaluation of guideline compliance")

class ScenarioAppropriateness(BaseModel):
    score: int = Field(..., ge=0, le=25, description="Context fit score (0-25)")
    analysis: str = Field(..., min_length=10, description="Evaluation of scenario relevance")

class SpeechMetric(BaseModel):
    score: int = Field(..., ge=0, le=10, description="Sub-score for delivery aspect (0-10)")
    analysis: str = Field(..., min_length=10, description="Technical evaluation of speech characteristic")

class ContentAnalysis(BaseModel):
    guideline_adherence: GuidelineAdherence
    scenario_appropriateness: ScenarioAppropriateness
    key_strengths: List[str] = Field(..., min_items=1, description="List of content strengths")
    improvement_areas: List[str] = Field(..., min_items=1, description="List of content weaknesses")

class DeliveryAnalysis(BaseModel):
    speech_pace: SpeechMetric
    clarity_pronunciation: SpeechMetric
    speech_flow: SpeechMetric
    volume_control: SpeechMetric

class ScoreSummary(BaseModel):
    content_alignment: int = Field(..., ge=0, le=25)
    scenario_appropriateness: int = Field(..., ge=0, le=25)
    communication_clarity: int = Field(..., ge=0, le=25)
    audio_delivery: int = Field(..., ge=0, le=25)
    total_score: int = Field(..., ge=0, le=100)

class GeneratedFeedback(BaseModel):
    """Structured evaluation of user's communication performance"""
    overall_performance: Literal["Excellent", "Good", "Fair", "Needs Improvement"]
    content_analysis: ContentAnalysis
    delivery_analysis: DeliveryAnalysis
    recommendations: List[str] = Field(
        ...,
        min_items=3,
        max_items=5,
        examples=[
            "Practice pausing after key points for emphasis",
            "Slow down to 160 WPM during technical explanations"
        ]
    )
    score_summary: ScoreSummary