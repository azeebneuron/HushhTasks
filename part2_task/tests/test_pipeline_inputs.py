# tests/test_pipeline_inputs.py
import asyncio
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processors.gemini_processor import GeminiProcessor
from processors.llama_processor import LlamaProcessor
from utils.comparison import ModelComparison
from utils.output_handler import OutputHandler
import json

async def test_processors():
    # Initialize processors and output handler
    gemini = GeminiProcessor()
    llama = LlamaProcessor()
    comparison_tool = ModelComparison()
    output_handler = OutputHandler()

    # Test cases
    test_cases = {
        "news_article": """
        Tesla has unveiled its latest electric vehicle, promising groundbreaking battery technology
        and enhanced autonomous driving capabilities. Industry experts are divided on the impact,
        with some praising the innovation while others question the timeline for delivery.
        """,
        "technical_blog": """
        Kubernetes has transformed container orchestration, enabling seamless scaling and 
        deployment of microservices. However, the learning curve remains steep, and organizations
        face challenges in maintaining complex clusters.
        """,
        "product_review": """
        The XPS 13 delivers exceptional performance in a compact form factor. Battery life
        exceeds expectations, lasting over 12 hours. However, the premium price point and
        limited port selection might deter some buyers.
        """
    }

    print("\nStarting analysis and saving results...")
    all_results = []

    for text_type, text in test_cases.items():
        print(f"\nProcessing: {text_type}")
        
        try:
            # Process with both models
            gemini_result = await gemini.process_text(text)
            llama_result = await llama.process_text(text)
            
            # Save individual results
            gemini_path = output_handler.save_result(
                gemini_result.model_dump(), 
                'gemini', 
                text_type
            )
            llama_path = output_handler.save_result(
                llama_result.model_dump(), 
                'llama', 
                text_type
            )
            
            # Generate and save comparison
            comparison = comparison_tool.compare_responses(gemini_result, llama_result)
            comparison['text_type'] = text_type
            comparison_path = output_handler.save_comparison(comparison, text_type)
            
            all_results.append(comparison)
            
            print(f"Results saved:")
            print(f"├── Gemini: {gemini_path}")
            print(f"├── LLaMA: {llama_path}")
            print(f"└── Comparison: {comparison_path}")
            
        except Exception as e:
            print(f"Error processing {text_type}: {str(e)}")

    # Generate final report
    report_path, csv_path = output_handler.generate_report(all_results)
    
    print("\nFinal Reports Generated:")
    print(f"├── Summary Report: {report_path}")
    print(f"└── Detailed CSV: {csv_path}")
    
    # Print summary to console
    with open(report_path, 'r') as f:
        summary = json.load(f)
        print("\nSummary Metrics:")
        print(json.dumps(summary['model_comparison'], indent=2))

if __name__ == "__main__":
    asyncio.run(test_processors())