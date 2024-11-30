# test_llama_processor.py
import asyncio
from processors.llama_processor import LlamaProcessor

async def test_processor():
    processor = LlamaProcessor()
    
    test_text = """Machine learning has revolutionized technology,
                   making significant impacts in various fields."""
    
    print("Testing LLaMA processor...")
    try:
        result = await processor.process_text(test_text)
        print("\nSuccess! Processed result:")
        print(result.model_dump())
        return True
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_processor())