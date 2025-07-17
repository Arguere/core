from typing import Dict
from app.services.llm_service import LLMService

class FeedbackGenerator:
    @staticmethod
    async def generate_feedback(transcription: str, framework_name: str, scenario_description: str) -> Dict[str, str]:
        try:
            # TODO: today we assume the llm as the context of the framework, 
            # in the future we might want to inject the framework context
            prompt = f"""
            
            You are a communication coach and feedback expert.

            A user just completed a communication roleplay using the {framework_name} method.

            Your job is to:

            Analyze the user’s message and check whether they followed the framework correctly.

            Provide clear, specific feedback:
            a. What they did well (in structure, tone, clarity, etc.)
            b. Suggestions to improve next time (based on the framework’s ideal application)

            Score their performance from 0 to 100, based on how well they applied the framework.

            Use the structure below in your answer.

            —

            Framework: {framework_name}

            Scenario Context:
            {scenario_description}
            (e.g., “Give feedback to a teammate who interrupted you during a meeting.”)

            User Response:
            {transcription}

            —

            Now give your evaluation:

            ✅ What the user did well:
            (Specific bullet points about tone, clarity, use of structure, presence, etc.)

            🔁 Suggestions to improve:
            (Specific corrections or guidance on missed or weak parts of the framework)

            🎯 Framework Score: __ / 100
            (Explain what contributed to the score)
            
            🎤 Recommended phrase to try next time:
            (One improved sentence they could say)
            """
   
            return await LLMService.get_completion(prompt)
        except Exception as e:
            raise Exception(f"Feedback generation failed: {str(e)}")