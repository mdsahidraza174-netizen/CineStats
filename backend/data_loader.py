import os
import pandas as pd


# ============================================================
# Data Loading Functions
# ============================================================

def load_movie_data():
    """Load movie booking data from CSV file."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "data", "movie_bookings.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Data loaded: {len(df)} records")
    
    return df


def get_showtime_popularity(df):
    """Calculate showtime popularity based on total seats booked."""
    showtime_popularity = df.groupby('show_time')['seats_booked'].sum()
    showtime_popularity = showtime_popularity.sort_values(ascending=False)
    
    return showtime_popularity


def get_summary_stats(df):
    """Calculate summary statistics for the dataset."""
    total_bookings = len(df)
    total_seats = df['seats_booked'].sum()
    total_revenue = (df['seats_booked'] * df['ticket_price']).sum()
    unique_movies = df['movie_name'].nunique()
    unique_cities = df['City'].nunique()
    
    summary = {
        "total_bookings": int(total_bookings),
        "total_seats": int(total_seats),
        "total_revenue": float(total_revenue),
        "unique_movies": int(unique_movies),
        "unique_cities": int(unique_cities)
    }
    
    return summary