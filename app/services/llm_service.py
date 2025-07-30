from typing import Dict
import aiohttp
from app.core.config import settings
from cerebras.cloud.sdk import Cerebras

class LLMService:
    @staticmethod
    async def get_completion(prompt: str) -> Dict:
        if not settings.CEREBRAS_API_KEY:
            raise ValueError("LLM API key is not set in the configuration.")
        
        try:
            # Initialize Cerebras client
            client = Cerebras(api_key=settings.CEREBRAS_API_KEY)
            
            stream = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }
                ],
                model="qwen-3-32b",
                stream=True,
                max_completion_tokens=16382,
                temperature=0.7,
                top_p=0.95,
            )
            # Collect the response
            response = ""
            async for chunk in stream:
                response += chunk["choices"][0]["message"]["content"]
                
            # print(chunk.choices[0].delta.content or "", end="")
            return {"text": response}
        except aiohttp.ClientError as e:
            raise Exception(f"LLM service connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"LLM service error: {str(e)}")
