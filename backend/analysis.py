import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ============================================================
# Core Analysis Functions
# ============================================================

def run_analysis(csv_path="data/movie_bookings.csv"):
    """
    Main analysis function for movie booking data.
    Returns summary statistics and generates visualization.
    """
    print("=" * 60)
    print("CineStats - Movie Ticket Booking Analysis")
    print("=" * 60)
    
    df = pd.read_csv(csv_path)
    
    print(f"\nData loaded successfully!")
    print(f"Total records found: {len(df)}")
    
    df["show_date"] = pd.to_datetime(df["show_date"])
    first_date = df["show_date"].min().strftime("%d %b %Y")
    last_date = df["show_date"].max().strftime("%d %b %Y")
    print(f"Data is from: {first_date} to {last_date}")
    
    print("\n" + "=" * 60)
    print("First 5 Records:")
    print("=" * 60)
    print(df.head())
    
    total_seats = int(df["seats_booked"].sum())
    print(f"\nTotal Seats Booked: {total_seats}")
    
    showtime_popularity = _analyze_showtime_popularity(df)
    
    most_popular_time = showtime_popularity.idxmax()
    max_seats = int(showtime_popularity.max())
    
    print("\n" + "=" * 60)
    print("Result:")
    print(f"Most Popular Show Time: {most_popular_time}")
    print(f"Total Seats Booked: {max_seats}")
    print("=" * 60)
    
    _generate_showtime_chart(showtime_popularity)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    
    return {
        'total_seats': total_seats,
        'most_popular_time': most_popular_time,
        'max_seats': max_seats,
        'first_date': first_date,
        'last_date': last_date
    }


def _analyze_showtime_popularity(df):
    """Analyze and display showtime popularity."""
    print("\n" + "=" * 60)
    print("Show-Time Popularity Analysis")
    print("=" * 60)
    
    showtime_popularity = df.groupby('show_time')['seats_booked'].sum()
    showtime_popularity_sorted = showtime_popularity.sort_values(ascending=False)
    
    print("\nTotal Seats Booked by Show Time:")
    print("-" * 40)
    for show_time, total_seats in showtime_popularity_sorted.items():
        print(f"{show_time:15} : {total_seats:6} seats")
    
    return showtime_popularity


def _generate_showtime_chart(showtime_popularity):
    """Generate and save showtime popularity bar chart."""
    print("\n" + "=" * 60)
    print("Generating Visualization...")
    print("=" * 60)
    
    time_order = ['10:00 AM', '1:00 PM', '4:00 PM', '7:00 PM', '10:00 PM']
    showtime_chronological = showtime_popularity.reindex(time_order)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_pos = np.arange(len(showtime_chronological))
    heights = showtime_chronological.values
    bar_width = 0.4
    
    for i, (x, height) in enumerate(zip(x_pos, heights)):
        rounded_bar = mpatches.FancyBboxPatch(
            (x - bar_width/2, 0), bar_width, height,
            boxstyle="round,pad=0.02",
            facecolor='#4f6cff',
            edgecolor='none'
        )
        ax.add_patch(rounded_bar)
    
    ax.set_xlim(-0.5, len(showtime_chronological) - 0.5)
    ax.set_ylim(0, max(heights) * 1.1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(showtime_chronological.index, rotation=0, ha='center')
    
    plt.title("Show-Time Popularity Based on Bookings", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Show Time", fontsize=12, labelpad=15)
    plt.ylabel("Total Seats Booked", fontsize=12, labelpad=15)
    plt.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.5)
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.set_facecolor("#ffffff")
    
    plt.tight_layout()
    
    os.makedirs("outputs/charts", exist_ok=True)
    output_path = "outputs/charts/showtime_popularity.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"\nChart saved successfully at: {output_path}")


# ============================================================
# City-wise Analysis Functions
# ============================================================

def get_all_cities(csv_path="data/movie_bookings.csv"):
    """Extract and return all unique cities sorted alphabetically."""
    df = pd.read_csv(csv_path)
    cities = sorted(df['City'].unique().tolist())
    return cities


def analyze_city_top_movies(csv_path, selected_city):
    """Generate bar chart for top 5 movies in selected city."""
    df = pd.read_csv(csv_path)
    city_data = df[df['City'] == selected_city].copy()
    
    movie_popularity = city_data.groupby('movie_name')['seats_booked'].sum()
    top_5_movies = movie_popularity.sort_values(ascending=False).head(5)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_pos = np.arange(len(top_5_movies))
    heights = top_5_movies.values
    bar_width = 0.3
    
    for i, (x, height) in enumerate(zip(x_pos, heights)):
        rounded_bar = mpatches.FancyBboxPatch(
            (x - bar_width/2, 0), bar_width, height,
            boxstyle="round,pad=0.02",
            facecolor='#4CAF50',
            edgecolor='none'
        )
        ax.add_patch(rounded_bar)
    
    ax.set_xlim(-0.5, len(top_5_movies) - 0.5)
    ax.set_ylim(0, max(heights) * 1.1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(top_5_movies.index, rotation=0, ha='right')
    
    plt.title(f"{selected_city}'s Top 5 Movies", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Movie Name", fontsize=12, labelpad=15)
    plt.ylabel("Total Seats Booked", fontsize=12, labelpad=15)
    plt.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.5)
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.set_facecolor("#ffffff")
    
    plt.tight_layout()
    
    os.makedirs("outputs/charts", exist_ok=True)
    output_path = "outputs/charts/city_top_movies.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path


def get_city_movie_details(csv_path, selected_city):
    """Get detailed analysis for selected city including chart, top movies, and summary."""
    df = pd.read_csv(csv_path)
    city_data = df[df['City'] == selected_city].copy()
    
    movie_popularity = city_data.groupby('movie_name')['seats_booked'].sum()
    top_5_movies = movie_popularity.sort_values(ascending=False).head(5)
    
    chart_path = analyze_city_top_movies(csv_path, selected_city)
    
    top_movies_list = [
        {"rank": rank, "name": movie_name, "seats": int(seats)}
        for rank, (movie_name, seats) in enumerate(top_5_movies.items(), 1)
    ]
    
    total_seats_city = int(city_data['seats_booked'].sum())
    total_movies = len(city_data['movie_name'].unique())
    summary = f"In {selected_city}, {total_movies} movies were screened with a total of {total_seats_city} seats booked."
    
    return {
        "chart_url": chart_path,
        "top_movies": top_movies_list,
        "summary": summary
    }


# ============================================================
# Main Execution
# ============================================================

if __name__ == "__main__":
    run_analysis()
    
    csv_path = "data/movie_bookings.csv"
    cities = get_all_cities(csv_path)
    
    print(f"\n\nTotal cities found: {len(cities)}")
    print("\nAll Cities (Alphabetically):")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")
    
    city_number = int(input("\nEnter city number: "))
    
    if 1 <= city_number <= len(cities):
        selected_city = cities[city_number - 1]
        chart_path = analyze_city_top_movies(csv_path, selected_city)
        print(f"\n✅ Chart saved: {chart_path}")
    else:
        print("❌ Invalid city number!")