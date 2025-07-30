from typing import Dict
from app.schemas.guideline import GeneratedGuideline
from app.services.llm_service import LLMService


class GuidelineGenerator:
    @staticmethod
    async def generate(context: str) -> Dict[str, str]: 
        try: 
            prompt = ""

            # return await LLMService.get_completion(prompt)
            return GeneratedGuideline(
                title="Sample Guideline Title",
                knowledge_foundation="This guideline is based on the following knowledge foundation: ...",
                guideline={
                    "Step 1 ": "Description",
                    "Step 2": "Description"
                }
            )
        except Exception as e:
            raise Exception(f"Guideline generation failed: {str(e)}")


