from typing import Dict
import aiohttp
from openai import AsyncOpenAI
from app.core.config import settings
import asyncio

class LLMService:
    @staticmethod
    async def get_completion(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.7, max_retries: int = 3) -> Dict:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set in the configuration.")
        
        for attempt in range(max_retries):
            try:
                client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

                response = await client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert communication coach with years of experience in evaluating and improving interpersonal communication skills."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=model,
                    temperature=temperature,
                    max_tokens=4000,
                    timeout=30.0
                )

                return {"text": response.choices[0].message.content}
        
            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise Exception("LLM service timeout after multiple attempts")
            
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                raise Exception(f"LLM service error: {str(e)}")
        
        raise Exception("LLM service failed after all retry attempts")

    @staticmethod
    async def get_structured_completion(prompt: str, response_format: str = "json") -> Dict:
        """Get completion with structured output format"""
        structured_prompt = f"""
{prompt}

IMPORTANT: Please provide your response in valid JSON format as specified in the prompt.
Ensure all JSON keys are properly quoted and the structure is valid.
"""
        
        return await LLMService.get_completion(structured_prompt, temperature=0.3)