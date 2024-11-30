from db_operations import SupabaseConnector
from data_generator import generate_mock_search_data, save_to_csv

def main():
    # Initialize Supabase connector
    db = SupabaseConnector()
    
    # Test connection
    if db.test_connection():
        # Create tables
        if db.create_tables():
            # Generate mock data and save to CSV
            print("Generating mock data...")
            df = generate_mock_search_data(days=30)
            csv_file = "mock_search_data.csv"
            save_to_csv(df, csv_file)
            
            # Load data into Supabase
            print("Loading data into Supabase...")
            if db.load_mock_data(csv_file):
                print("Setup complete! All data has been loaded successfully.")
            else:
                print("Failed to load data.")
        else:
            print("Failed to create tables.")
    else:
        print("Failed to connect to Supabase. Please check your credentials.")

if __name__ == "__main__":
    main()