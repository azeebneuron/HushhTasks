import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

def generate_mock_search_data(days=30, queries_per_day=100):
    # Sample search queries with categories
    product_queries = [
        "blue jeans", "wireless headphones", "running shoes", "laptop bag",
        "gaming mouse", "yoga mat", "water bottle", "phone case",
        "desk chair", "coffee maker"
    ]
    
    tech_queries = [
        "javascript tutorial", "python basics", "react components",
        "sql queries", "docker basics", "git commands", "aws tutorial",
        "css flexbox", "api testing", "data structures"
    ]
    
    info_queries = [
        "how to cook pasta", "best practices coding", "what is machine learning",
        "how to start gym", "basic photography tips", "home organization",
        "time management tips", "healthy breakfast ideas", "meditation guide",
        "productivity hacks"
    ]
    
    all_queries = product_queries + tech_queries + info_queries
    
    # Generate date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    dates = [start_date + timedelta(days=x) for x in range(days)]
    
    data = []
    
    for date in dates:
        # Generate more entries for weekdays
        daily_queries = queries_per_day if date.weekday() < 5 else int(queries_per_day * 0.7)
        
        for _ in range(daily_queries):
            query = random.choice(all_queries)
            
            # Base impressions and clicks based on query type
            if query in product_queries:
                base_impressions = random.randint(50, 200)
                ctr_base = 0.15  # Higher CTR for product queries
            elif query in tech_queries:
                base_impressions = random.randint(30, 150)
                ctr_base = 0.10
            else:  # info queries
                base_impressions = random.randint(20, 100)
                ctr_base = 0.05
            
            # Add some randomness
            impressions = base_impressions + random.randint(-10, 10)
            ctr = max(0, min(1, ctr_base + random.uniform(-0.02, 0.02)))
            clicks = int(impressions * ctr)
            
            data.append({
                'search_query': query,
                'clicks': clicks,
                'impressions': impressions,
                'click_through_rate': round(ctr, 4),
                'search_date': date
            })
    
    return pd.DataFrame(data)

def save_to_csv(df, filename='mock_search_data.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    print(f"Total records: {len(df)}")
    print("\nSample data:")
    print(df.head())
    print("\nSummary statistics:")
    print(df.describe())

# Generate and save the data
df = generate_mock_search_data(days=30)
save_to_csv(df)