from analytics import SearchAnalytics

def main():
    analytics = SearchAnalytics()
    
    # Test daily CTR
    print("\n=== Daily CTR ===")
    daily_ctr = analytics.get_daily_ctr()
    if daily_ctr:
        for day in daily_ctr[:5]:  # Show first 5 days
            print(f"Date: {day['search_date']}, CTR: {day['avg_ctr']:.2%}")
    
    # Test top performing queries
    print("\n=== Top Performing Queries ===")
    top_queries = analytics.get_top_performing_queries()
    if top_queries:
        for query in top_queries:
            print(f"Query: {query['search_query']}")
            print(f"Avg CTR: {query['avg_ctr']:.2%}")
            print(f"Total Impressions: {query['total_impressions']}")
            print("---")
    
    # Test low performing queries
    print("\n=== Low Performing Queries ===")
    low_performing = analytics.get_low_performing_queries()
    if low_performing:
        for query in low_performing:
            print(f"Query: {query['search_query']}")
            print(f"Avg CTR: {query['avg_ctr']:.2%}")
            print(f"Total Impressions: {query['total_impressions']}")
            print("---")
    
    # Save daily insights
    print("\n=== Saving Daily Insights ===")
    insights = analytics.save_daily_insights()
    if insights:
        print("Successfully saved insights for date:", insights['insight_date'])

if __name__ == "__main__":
    main()