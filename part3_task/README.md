# Search Analytics Pipeline

## Overview
This project implements an automated search analytics pipeline that processes and analyzes search and click data. It calculates daily click-through rates (CTR), identifies top-performing search queries, and detects queries that might need optimization.

## Project Structure
```
search_analytics/
├── data_generator.py     # Generates mock search data
├── db_operations.py      # Handles database operations
├── analytics.py         # Core analytics logic
├── run_analytics.py     # Cron job script
├── analytics.log        # Execution logs
├── requirements.txt     # Project dependencies
└── .env                # Environment variables
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Supabase account (free tier)
- Cron (Linux/Unix)

### Installation
1. Clone the repository:

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with Supabase credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Database Setup
1. Create required tables in Supabase:
```sql
-- Search clicks table
CREATE TABLE search_clicks (
    search_id SERIAL PRIMARY KEY,
    search_query VARCHAR(255),
    clicks INT DEFAULT 0,
    impressions INT DEFAULT 0,
    click_through_rate FLOAT,
    search_date DATE DEFAULT CURRENT_DATE
);

-- Insights table
CREATE TABLE search_insights (
    id SERIAL PRIMARY KEY,
    insight_date DATE,
    average_ctr FLOAT,
    top_queries JSONB,
    low_performance_queries JSONB
);
```

## Running the Pipeline

### Generate Mock Data
```bash
python data_generator.py
```

### Run Analytics Manually
```bash
python run_analytics.py
```

### Set Up Automated Analysis
1. Open crontab:
```bash
crontab -e
```

2. Add daily midnight run:
```bash
0 0 * * * /path/to/venv/bin/python /path/to/search_analytics/run_analytics.py >> /path/to/search_analytics/cron.log 2>&1
```

## Analytics Features

### Daily CTR Analysis
- Calculates average click-through rate per day
- Tracks trends over time
- Stores historical data

### Top Performing Queries
- Identifies top 5 queries by CTR
- Includes minimum impression threshold
- Updates daily

### Low Performance Detection
- Finds queries with high impressions but low CTR
- Helps identify optimization opportunities
- Configurable thresholds

## Monitoring
- Check execution logs:
```bash
tail -f analytics.log
```

- View cron job logs:
```bash
tail -f cron.log
```

## File Descriptions
- `data_generator.py`: Creates realistic mock search data
- `db_operations.py`: Handles Supabase database operations
- `analytics.py`: Contains core analytics logic
- `run_analytics.py`: Script executed by cron job

## Dependencies
- pandas
- python-dotenv
- supabase
- schedule

## Error Handling
- Comprehensive logging
- Failed job notifications
- Automatic retry mechanism

## Maintenance
- Logs are automatically created in the project directory
- Old logs are not automatically cleaned up
- Monitor disk space regularly
