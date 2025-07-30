from typing import Dict, Any
from app.services.llm_service import LLMService
import json

class FeedbackGenerator:
    @staticmethod
    async def generate(
        transcription: str,
        scenario_context: str,
        guideline: Dict[str, str],
        audio_metrics: Dict[str, Any]
    ) -> str: 
        try: 
            # Convert guideline dict to readable format
            guideline_text = "\n".join([f"- {key}: {value}" for key, value in guideline.items()])
            
            prompt = f"""You are an expert communication coach evaluating a user's performance in a specific scenario.

SCENARIO CONTEXT:
{scenario_context}

COMMUNICATION GUIDELINES TO FOLLOW:
{guideline_text}

USER'S ACTUAL RESPONSE (TRANSCRIPTION):
"{transcription}"

AUDIO QUALITY METRICS:
- Speech Rate: {audio_metrics.get('speech_rate', 0):.1f} words per minute
- Duration: {audio_metrics.get('duration', 0):.1f} seconds
- Audio Clarity Score: {audio_metrics.get('spectral_clarity', 0):.1f}
- Pronunciation Accuracy: {audio_metrics.get('asr_accuracy', 0):.1f}%
- Speech Flow Score: {audio_metrics.get('pause_analysis', 0):.1f}%
- Volume Consistency: {audio_metrics.get('volume_consistency', 0):.1f}%
- Overall Audio Score: {audio_metrics.get('overall_score', 0):.1f}/100

EVALUATION CRITERIA:
1. Content Alignment: How well does the response follow the provided guidelines?
2. Scenario Appropriateness: Is the response suitable for the given context?
3. Communication Effectiveness: Is the message clear and well-structured?
4. Audio Quality: How is the speech delivery (pace, clarity, consistency)?

Please provide comprehensive feedback in the following structure:

**OVERALL PERFORMANCE: [Excellent/Good/Fair/Needs Improvement]**

**CONTENT ANALYSIS:**
- Guideline Adherence: [Analyze how well they followed each guideline point]
- Scenario Appropriateness: [Evaluate if response fits the context]
- Key Strengths: [What they did well]
- Areas for Improvement: [What needs work]

**DELIVERY ANALYSIS:**
- Speech Pace: [Comment on their speaking speed - optimal is 140-180 WPM]
- Clarity and Pronunciation: [Based on ASR accuracy and spectral clarity]
- Speech Flow: [Comment on pauses and rhythm]
- Volume Control: [Consistency in volume]

**SPECIFIC RECOMMENDATIONS:**
[Provide 3-5 specific, actionable recommendations for improvement]

**SCORE BREAKDOWN:**
- Content Alignment: __/25
- Scenario Appropriateness: __/25  
- Communication Clarity: __/25
- Audio Delivery: __/25
- **TOTAL SCORE: __/100**

Keep the feedback constructive, specific, and encouraging. Focus on actionable improvements the user can make."""

            response = await LLMService.get_completion(prompt)
            return response.get("text", "Failed to generate feedback")
            
        except Exception as e:
            raise Exception(f"Feedback generation failed: {str(e)}")

    @staticmethod
    async def generate_followup_questions(
        transcription: str,
        scenario_context: str,
        guideline: Dict[str, str],
        feedback_score: float
    ) -> str:
        """Generate follow-up questions or exercises based on performance"""
        try:
            guideline_text = "\n".join([f"- {key}: {value}" for key, value in guideline.items()])
            
            prompt = f"""Based on the user's performance in this communication scenario, generate 3-5 follow-up questions or practice exercises to help them improve.

SCENARIO CONTEXT:
{scenario_context}

GUIDELINES THEY WERE SUPPOSED TO FOLLOW:
{guideline_text}

USER'S RESPONSE:
"{transcription}"

PERFORMANCE LEVEL: {feedback_score}/100

Generate follow-up content that:
1. Addresses their specific weaknesses
2. Reinforces the guidelines they struggled with
3. Provides progressive difficulty
4. Encourages practical application

Format as:
**FOLLOW-UP EXERCISES:**
1. [Exercise/Question 1]
2. [Exercise/Question 2]
3. [Exercise/Question 3]
...

**PRACTICE SCENARIOS:**
- [Related scenario 1]
- [Related scenario 2]
...

Keep suggestions practical and achievable."""

            response = await LLMService.get_completion(prompt)
            return response.get("text", "Failed to generate follow-up questions")
            
        except Exception as e:
            raise Exception(f"Follow-up generation failed: {str(e)}")