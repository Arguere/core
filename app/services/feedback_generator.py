from typing import Dict
from services.llm_service import LLMService


class FeedbackGenerator:
    @staticmethod
    async def generate() -> Dict[str, str]: 
        try: 
            prompt = ""

            return await LLMService.get_completion(prompt)
        except Exception as e:
            raise Exception(f"Feedback generation failed: {str(e)}")


