# Technical Assessment Tasks

A collection of three backend development tasks demonstrating proficiency in API development, data processing pipelines, and SQL analytics.

## Project Structure

```
HushhTask/
├── part1_task/     # FastAPI CRUD API
├── part2_task/     # LLM Data Processing Pipeline
└── part3_task/     # SQL Analytics with Supabase
```

## Part 1: CRUD Operations API Development

A FastAPI-based CRUD API for managing users and orders with comprehensive testing, error handling, and performance optimization.

### Key Features
- Complete CRUD operations for users and orders
- Asynchronous database operations
- Comprehensive error handling
- SSL security implementation
- Concurrent request handling with Uvicorn/Gunicorn
- Extensive test coverage

[View Part 1 Details](./part1_task/README.md)

## Part 2: Data Processing Pipeline with APIs

A data processing pipeline integrating OpenAI/Gemini API with local LLM comparison capabilities.

### Key Features
- OpenAI/Gemini API integration
- Custom prompt engineering
- Pydantic validation models
- Local LLM (LLaMA) setup and comparison
- Comprehensive error handling
- Rate limit management

[View Part 2 Details](./part2_task/README.md)

## Part 3: Metrics Extraction and SQL Analytics

An automated SQL analytics pipeline using Supabase for analyzing search and click-through metrics.

### Key Features
- Daily CTR analysis
- Top performing queries identification
- Low performance query detection
- Automated insights generation
- Scheduled pipeline execution
- Mock data generation scripts

[View Part 3 Details](./part3_task/README.md)

## Technology Stack

- **Backend Framework**: FastAPI
- **Databases**: 
  - PostgreSQL
  - Supabase
- **AI/ML**: 
  - OpenAI API
  - Gemini API
  - Local LLaMA
- **Testing**: pytest
- **Automation**: Celery/cron
- **Documentation**: Swagger/OpenAPI

## Getting Started

Each subdirectory contains its own setup instructions, requirements, and documentation. Please refer to the individual README files in each directory for specific setup and running instructions.

1. Clone the repository with submodules:
```bash
git clone --recursive https://github.com/yourusername/HushhTask.git
cd HushhTask
```

2. Set up individual projects:
```bash
# For Part 1
cd part1_task
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Repeat for part2_task and part3_task
```

## Project Status (November 29 - Present)
### Implementation Status

* Part 1: CRUD API Development
   * ✅ Basic CRUD Operations
   * ✅ Error Handling
   * ✅ Testing
   * ⏳ SSL Implementation
   * ⏳ Async Operations

* Part 2: Data Processing Pipeline
   * ✅ API Integration
   * ✅ Local LLM Setup
   * ✅ Comparison Report
   * ✅ Testing

* Part 3: SQL Analytics
   * ✅ Database Setup
   * ✅ Query Development
   * ✅ Automation Pipeline
   * ✅ Testing

## Note

Each subdirectory maintains its own Git history. Please refer to individual contribution guidelines in each project's README.

## Contact

For any queries regarding this assessment, please contact srahulsingh7488@gmail.com.