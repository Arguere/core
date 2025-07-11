from typing import Dict
from app.services.llm_service import LLMService

class FeedbackGenerator:
    @staticmethod
    async def generate_feedback(submission_data: Dict, analysis_results: Dict) -> Dict[str, str]:
        try:
            content_type = submission_data.get("content_type")
            content = submission_data.get("content_path")
            
            prompt = f"""
            Analyze the following {content_type} submission and provide feedback:
            
            Content: {content}
            Speech Rate: {analysis_results.get('speech_rate', 'N/A')} words/min
            Duration: {analysis_results.get('duration', 'N/A')} seconds
            Spectral Clarity: {analysis_results.get('spectral_clarity', 'N/A')}
            ASR Accuracy: {analysis_results.get('asr_accuracy', 'N/A')}
            Score: {analysis_results.get('score', 'N/A')}
            
            Provide feedback in two sections:
            1. What you did well
            2. Suggestions to improve
            """
   
            return await LLMService.get_completion(prompt)
        except Exception as e:
            raise Exception(f"Feedback generation failed: {str(e)}")