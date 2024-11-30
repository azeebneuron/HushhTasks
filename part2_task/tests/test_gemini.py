# test_gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

async def test_gemini():
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        return False
        
    print(f"API Key found: {api_key[:4]}...{api_key[-4:]}")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = await model.generate_content_async("Return this exact JSON: {\"test\": \"success\"}")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"Error testing Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_gemini())