from typing import Dict
from services.llm_service import LLMService


class FollowUpGenerator:
    @staticmethod
    async def generate() -> Dict[str, str]: 
        try: 
            prompt = ""

            return await LLMService.get_completion(prompt)
        except Exception as e:
            raise Exception(f"FollowUp Questions generation failed: {str(e)}")
