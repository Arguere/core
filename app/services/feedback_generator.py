from typing import Dict, Any
from app.schemas.feedback import GeneretedFeedback
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
            
            input_fields = {
                "scenario_context": "Description of the communication scenario (e.g., 'Sales pitch to investors')",
                "guideline_text": "Specific guidelines the user was asked to follow (bullet points or text)",
                "transcription": "Exact user response transcription",
                "audio_metrics": {
                    "speech_rate": "Words per minute (float)",
                    "duration": "Duration in seconds (float)",
                    "spectral_clarity": "0-100 score (float)",
                    "asr_accuracy": "Pronunciation accuracy % (float)",
                    "pause_analysis": "Speech flow score % (float)",
                    "volume_consistency": "Volume stability % (float)",
                    "overall_score": "Composite audio quality 0-100 (float)"
                }
            }

            output_structure = {
                "overall_performance": "Excellent/Good/Fair/Needs Improvement",
                "content_analysis": {
                    "guideline_adherence": {
                        "score": "0-25 (int)",
                        "analysis": "Detailed comments on guideline alignment"
                    },
                    "scenario_appropriateness": {
                        "score": "0-25 (int)",
                        "analysis": "Evaluation of context fit"
                    },
                    "key_strengths": ["List of strengths (bullet points)"],
                    "improvement_areas": ["List of weaknesses (bullet points)"]
                },
                "delivery_analysis": {
                    "speech_pace": {
                        "score": "0-10 (int)",
                        "analysis": "Comments on WPM vs ideal 140-180 range"
                    },
                    "clarity_pronunciation": {
                        "score": "0-10 (int)",
                        "analysis": "Based on ASR accuracy and spectral clarity"
                    },
                    "speech_flow": {
                        "score": "0-10 (int)",
                        "analysis": "Pause/rhythm evaluation"
                    },
                    "volume_control": {
                        "score": "0-10 (int)",
                        "analysis": "Consistency notes"
                    }
                },
                "recommendations": [
                    "3-5 actionable improvement suggestions"
                ],
                "score_summary": {
                    "content_alignment": "0-25 (int)",
                    "scenario_appropriateness": "0-25 (int)",
                    "communication_clarity": "0-25 (int)",
                    "audio_delivery": "0-25 (int)",
                    "total_score": "0-100 (int)"
                }
            }

            rules = [
                "Use same language as user's transcription",
                "Convert all scores to integers (round decimals)",
                "Prioritize actionable feedback over generic praise",
                "Reference specific transcription segments when critiquing (e.g., 'At 0:32, you...')"
            ]

            context = {
                "scenario_context": scenario_context,
                "guideline_text": guideline_text,
                "transcription": transcription,
                "audio_metrics": audio_metrics
            }

            prompt = json.dumps({
                "role": "communication_coach",
                "task": "Evaluate user's performance against guidelines and audio metrics, returning structured feedback.",
                "input_fields": input_fields,
                "output_structure": output_structure,
                "rules": rules,
                "context": context
            }, indent=4)

            response = await LLMService.get_completion(prompt)
            response_text = response.get("text", "").strip()
            
            # Try to parse JSON response
            try:
                parsed_response = json.loads(response_text)
                if not isinstance(parsed_response, dict):
                    raise ValueError("Response is not a valid JSON object")
                return GeneretedFeedback(**parsed_response)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON response from LLM: {response_text}")
            except ValueError as ve:
                raise ValueError(f"Response parsing error: {str(ve)}")
            
        except Exception as e:
            raise Exception(f"Feedback generation failed: {str(e)}")

  