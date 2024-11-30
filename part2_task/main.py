# main.py
import asyncio
import os
from datetime import datetime
from processors.gemini_processor import GeminiProcessor
from processors.llama_processor import LlamaProcessor
from utils.comparison import ModelComparison
from dotenv import load_dotenv
import json

load_dotenv()

class Pipeline:
    def __init__(self):
        """Initialize processing pipeline"""
        print("Initializing processors...")
        self.gemini_processor = GeminiProcessor()
        self.llama_processor = LlamaProcessor()
        self.comparison_tool = ModelComparison()
        
        # Create output directories
        os.makedirs('output/processed', exist_ok=True)
        os.makedirs('output/comparisons', exist_ok=True)

    async def process_single(self, text: str) -> dict:
        """Process single text through both models"""
        try:
            print("\nProcessing with Gemini...")
            gemini_result = await self.gemini_processor.process_text(text)
            print("Gemini processing complete.")
            print("Gemini result:", gemini_result.model_dump())  # Updated from dict() to model_dump()

            print("\nProcessing with LLaMA...")
            llama_result = await self.llama_processor.process_text(text)
            print("LLaMA processing complete.")
            print("LLaMA result:", llama_result.model_dump())  # Updated from dict() to model_dump()
            
            # Compare results
            comparison = self.comparison_tool.compare_responses(
                gemini_result, 
                llama_result
            )
            
            # Save comparison
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f'output/comparisons/comparison_{timestamp}.json'
            
            # Save with pretty printing
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(comparison, f, indent=2, default=str)
            
            print(f"\nComparison saved to: {filepath}")
            return comparison
            
        except Exception as e:
            print(f"Error in pipeline: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None

async def main():
    print("Starting the pipeline...")
    pipeline = Pipeline()
    
    # Test text
    text = """
    Machine learning has revolutionized the tech industry, enabling breakthroughs
    in natural language processing, computer vision, and autonomous systems.
    However, challenges remain in areas such as bias mitigation and model interpretability.
    """
    
    print("\nProcessing text sample...")
    result = await pipeline.process_single(text)
    
    if result:
        print("\nProcessing complete! Final comparison:")
        print(json.dumps(result, indent=2, default=str))
        
        # Print the location of the saved comparison
        print("\nResults have been saved to the output directory.")
    else:
        print("\nProcessing failed! Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())