# processors/gemini_processor.py
import google.generativeai as genai
from datetime import datetime
from .base_processor import BaseProcessor
from models.pydantic_models import ProcessedData
import os
from dotenv import load_dotenv
import json

load_dotenv()

class GeminiProcessor(BaseProcessor):
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # New structured prompt
        self.prompt_template = """You are a text analysis system. Analyze the following text and provide the results in JSON format.

TEXT TO ANALYZE:
{text}

INSTRUCTIONS:
1. Return ONLY a valid JSON object
2. Include exactly these fields:
   - sentiment (string: "positive", "negative", or "neutral")
   - key_topics (array of strings)
   - summary (string)
   - confidence_score (number between 0 and 1)
3. Do not include any explanations or additional text
4. Ensure the output is valid JSON

Example of expected format:
{{"sentiment": "positive", "key_topics": ["AI", "technology"], "summary": "Brief summary here", "confidence_score": 0.85}}
"""

    async def process_text(self, text: str) -> ProcessedData:
        """Process text using Gemini API"""
        try:
            # Set specific generation config
            generation_config = {
                "temperature": 0.1,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }

            # Generate response
            response = await self.model.generate_content_async(
                contents=self.prompt_template.format(text=text),
                generation_config=generation_config,
            )

            # Print raw response for debugging
            print("\nRaw Gemini response:", response.text)

            # Clean and parse response
            response_text = response.text.strip()
            
            # Extract JSON from response
            try:
                # Try direct JSON parsing first
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to find JSON in the text
                try:
                    start_idx = response_text.find('{')
                    end_idx = response_text.rfind('}') + 1
                    if start_idx != -1 and end_idx > 0:
                        json_str = response_text[start_idx:end_idx]
                        result = json.loads(json_str)
                    else:
                        raise ValueError("No JSON object found in response")
                except Exception as e:
                    print(f"Failed to extract JSON: {str(e)}")
                    raise

            # Validate and clean the result
            result['sentiment'] = result['sentiment'].lower()
            if result['sentiment'] not in ['positive', 'negative', 'neutral']:
                result['sentiment'] = 'neutral'

            result['confidence_score'] = float(result['confidence_score'])
            result['confidence_score'] = max(0.0, min(1.0, result['confidence_score']))

            if not isinstance(result['key_topics'], list):
                result['key_topics'] = [str(result['key_topics'])]

            result['timestamp'] = datetime.now()

            # Create ProcessedData object
            return ProcessedData(**result)

        except Exception as e:
            print(f"Error in Gemini processing: {str(e)}")
            print(f"Response text: {response.text if 'response' in locals() else 'No response generated'}")
            raise

    async def batch_process(self, texts: list[str]) -> list[ProcessedData]:
        results = []
        for text in texts:
            try:
                result = await self.process_text(text)
                results.append(result)
            except Exception as e:
                print(f"Error in batch processing: {str(e)}")
                results.append(None)
        return results

    def validate_response(self, response: dict) -> bool:
        required_fields = {'sentiment', 'key_topics', 'summary', 'confidence_score'}
        return all(field in response for field in required_fields)

    async def get_model_info(self) -> dict:
        return {
            "model_name": "gemini-pro",
            "temperature": 0.1,
            "top_p": 0.8,
            "top_k": 40
        }