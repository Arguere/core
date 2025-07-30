from typing import Dict
import aiohttp
from openai import AsyncOpenAI
from app.core.config import settings

class LLMService:
    @staticmethod
    async def get_completion(prompt: str) -> Dict:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set in the configuration.")
        
        try:
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

            stream = await client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }
                ],
                model="gpt-4",  # ou "gpt-4o", "gpt-3.5-turbo", etc
                stream=True,
                temperature=0.7,
                top_p=0.95,
                max_tokens=16382,
            )

            response = ""
            async for chunk in stream:
                delta = chunk.choices[0].delta
                response += delta.content if delta.content else ""

            return {"text": response}
        
        except aiohttp.ClientError as e:
            raise Exception(f"LLM service connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"LLM service error: {str(e)}")
