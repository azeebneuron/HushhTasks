#!/usr/bin/env python3
from analytics import SearchAnalytics
import logging
from datetime import datetime
import os
import json

# Get the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, 'analytics.log')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def format_query_info(queries):
    """Format query information for logging"""
    if not queries:
        return "No data available"
    
    result = []
    for query in queries:
        result.append(
            f"Query: {query['search_query']}, "
            f"CTR: {float(query['avg_ctr']):.2%}, "
            f"Impressions: {query['total_impressions']}"
        )
    return "\n    ".join(result)

def main():
    """Run the analytics job"""
    try:
        logging.info("Starting daily analytics job")
        
        # Run analytics
        analytics = SearchAnalytics()
        insights = analytics.save_daily_insights()
        
        if insights:
            logging.info(f"\nAnalytics Results for {insights['insight_date']}:")
            logging.info(f"\n1. Daily Average CTR: {insights['average_ctr']:.2%}")
            
            # Log top performing queries
            top_queries = json.loads(insights['top_queries'])
            logging.info("\n2. Top Performing Queries:")
            logging.info("    " + format_query_info(top_queries))
            
            # Log low performing queries
            low_perf_queries = json.loads(insights['low_performance_queries'])
            logging.info("\n3. Queries Needing Optimization:")
            logging.info("    " + format_query_info(low_perf_queries))
            
            logging.info("\nJob completed successfully")
        else:
            logging.error("Failed to generate insights")
            
    except Exception as e:
        logging.error(f"Error in analytics job: {str(e)}")
        raise

if __name__ == "__main__":
    main()