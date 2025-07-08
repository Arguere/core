from typing import Dict
import aiohttp
from app.core.config import settings

class LLMService:
    @staticmethod
    async def get_completion(prompt: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            try:
                headers = {
                    "Authorization": f"Bearer {settings.LLM_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "your-llm-model",  # Specify your LLM model
                    "prompt": prompt,
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                
                async with session.post(
                    "https://api.llm-provider.com/v1/completions",  # TODO: Replace with actual LLM API endpoint
                    json=data,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("choices", [{}])[0].get("text", {})
                    else:
                        raise Exception(f"LLM API error: {response.status}")
            except Exception as e:
                raise Exception(f"LLM service error: {str(e)}")