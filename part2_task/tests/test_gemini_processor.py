# test_gemini_processor.py
import asyncio
from processors.gemini_processor import GeminiProcessor

async def test_processor():
    processor = GeminiProcessor()
    
    test_text = """Machine learning has revolutionized technology,
                   making significant impacts in various fields."""
    
    print("Testing Gemini processor...")
    try:
        result = await processor.process_text(test_text)
        print("\nSuccess! Processed result:")
        print(result.dict())
        return True
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_processor())