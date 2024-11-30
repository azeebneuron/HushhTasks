# Text Processing Pipeline

A data processing pipeline that integrates OpenAI/Gemini API and LLaMA for processing unstructured text data into structured JSON format. The pipeline includes comparison capabilities between the models and comprehensive output handling.

## Project Structure
```
text_processing_pipeline/
├── utils/
│   ├── comparison.py        # Model output comparison utilities
│   ├── error_handlers.py    # Error handling utilities
│   ├── prompt_templates.py  # Model prompts
│   └── output_handler.py    # Results and report handling
├── models/
│   ├── pydantic_models.py   # Data validation models
│   └── llama/              # Local LLaMA model files
├── processors/
│   ├── base_processor.py    # Abstract processor class
│   ├── gemini_processor.py  # Google Gemini implementation
│   └── llama_processor.py   # LLaMA implementation
├── tests/
│   └── test_pipeline_inputs.py  # Pipeline tests
├── output/                  
│   ├── raw_results/         # Individual model outputs
│   ├── comparisons/         # Model comparisons
│   ├── reports/            # Analysis reports
│   └── visualizations/     # Data visualizations
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
└── main.py                # Main entry point
```

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
venv\Scripts\activate     # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
LLAMA_MODEL_PATH=models/llama/llama-2-7b-chat.Q4_K_M.gguf
```

4. Download LLaMA model:
```bash
python -m tests.test_llama_processor
```

## Usage

1. Run the main pipeline:
```bash
python main.py
```

2. Run tests with sample inputs:
```bash
python -m tests.test_pipeline_inputs
```

## Features

- Processes unstructured text into structured JSON format
- Integrates both Google Gemini and LLaMA models
- Compares outputs between models
- Generates detailed analysis reports
- Handles various types of input text:
  - News articles
  - Technical blogs
  - Product reviews
  - Social media posts

## Output Format

The pipeline generates structured JSON with the following fields:
```json
{
    "sentiment": "positive/negative/neutral",
    "key_topics": ["topic1", "topic2", ...],
    "summary": "Brief summary of the text",
    "confidence_score": 0.0-1.0
}
```

## Requirements

- Python 3.8+
- Google Gemini API key
- ~4GB disk space for LLaMA model
- Required packages listed in requirements.txt
