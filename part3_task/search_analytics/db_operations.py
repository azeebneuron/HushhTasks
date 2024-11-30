import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
import time

# Load environment variables
load_dotenv()

class SupabaseConnector:
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(self.url, self.key)

    def create_tables(self):
        """Create the required tables in Supabase"""
        try:
            # For Supabase, we'll need to create tables through the web interface
            # or using database migrations. Here we'll just verify if tables exist
            result = self.supabase.table('search_clicks').select("*").limit(1).execute()
            print("search_clicks table exists!")
            
            result = self.supabase.table('search_insights').select("*").limit(1).execute()
            print("search_insights table exists!")
            
            return True
            
        except Exception as e:
            print(f"Error checking tables: {str(e)}")
            print("Please create the tables using the Supabase web interface.")
            return False

    def load_mock_data(self, csv_file: str):
        """Load mock data from CSV into search_clicks table"""
        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Convert search_date to string format
            df['search_date'] = pd.to_datetime(df['search_date']).dt.strftime('%Y-%m-%d')
            
            # Convert DataFrame to list of dictionaries
            records = df.to_dict('records')
            
            # Insert data in batches of 100
            batch_size = 100
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                self.supabase.table('search_clicks').insert(batch).execute()
                print(f"Loaded batch {i//batch_size + 1}/{(len(records)-1)//batch_size + 1}")
            
            print(f"Successfully loaded {len(records)} records into search_clicks table")
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False

    def test_connection(self):
        """Test the Supabase connection"""
        try:
            # Test connection by trying to access the table
            result = self.supabase.table('search_clicks').select("*").limit(1).execute()
            print("Successfully connected to Supabase!")
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            print("Please make sure to create the tables in Supabase first.")
            return False