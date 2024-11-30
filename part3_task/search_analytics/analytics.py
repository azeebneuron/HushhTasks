import json
from db_operations import SupabaseConnector

class SearchAnalytics:
    def __init__(self):
        self.db = SupabaseConnector()
    
    def get_daily_ctr(self):
        """Calculate average CTR for each day"""
        try:
            query = """
            SELECT 
                search_date,
                AVG(click_through_rate) as avg_ctr
            FROM search_clicks
            GROUP BY search_date
            ORDER BY search_date;
            """
            
            result = self.db.supabase.rpc('get_daily_ctr', {}).execute()
            return result.data
        except Exception as e:
            print(f"Error calculating daily CTR: {str(e)}")
            return None

    def get_top_performing_queries(self, days=7, limit=5):
        """Find top performing queries by CTR"""
        try:
            query = """
            SELECT 
                search_query,
                AVG(click_through_rate) as avg_ctr,
                SUM(impressions) as total_impressions
            FROM search_clicks
            GROUP BY search_query
            HAVING SUM(impressions) >= 50
            ORDER BY avg_ctr DESC
            LIMIT 5;
            """
            
            result = self.db.supabase.rpc('get_top_queries', {}).execute()
            return result.data
        except Exception as e:
            print(f"Error finding top queries: {str(e)}")
            return None

    def get_low_performing_queries(self, min_impressions=100, max_ctr=0.05):
        """Find queries with high impressions but low CTR"""
        try:
            query = """
            SELECT 
                search_query,
                AVG(click_through_rate) as avg_ctr,
                SUM(impressions) as total_impressions
            FROM search_clicks
            GROUP BY search_query
            HAVING SUM(impressions) >= $1 AND AVG(click_through_rate) <= $2
            ORDER BY total_impressions DESC;
            """
            
            result = self.db.supabase.rpc('get_low_performing', {
                'min_impressions': min_impressions,
                'max_ctr': max_ctr
            }).execute()
            return result.data
        except Exception as e:
            print(f"Error finding low performing queries: {str(e)}")
            return None

    def save_daily_insights(self):
        """Save daily insights to search_insights table"""
        try:
            # Get various insights
            daily_ctr = self.get_daily_ctr()
            if not daily_ctr:
                raise Exception("No daily CTR data available")
                
            top_queries = self.get_top_performing_queries()
            low_performing = self.get_low_performing_queries()
            
            # Prepare insights data
            insights_data = {
                'insight_date': daily_ctr[-1]['search_date'],
                'average_ctr': daily_ctr[-1]['avg_ctr'],
                'top_queries': json.dumps(top_queries) if top_queries else None,
                'low_performance_queries': json.dumps(low_performing) if low_performing else None
            }
            
            # Save to search_insights table
            self.db.supabase.table('search_insights').insert(insights_data).execute()
            print("Daily insights saved successfully!")
            
            return insights_data
        except Exception as e:
            print(f"Error saving insights: {str(e)}")
            return None