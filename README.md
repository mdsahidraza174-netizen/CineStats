# CineStats — Movie Booking Data Analytics Dashboard

CineStats is a data analytics web application that allows users to upload a CSV file containing movie booking data and instantly generate meaningful insights and visualizations.
The project focuses on clean analysis, dynamic visualization, and interactive city-wise insights, built using Python, Pandas, and Matplotlib.

## Features

1. **CSV Upload Interface**
   - Upload movie booking datasets directly through a modern web UI.

2. **Show-Time Popularity Analysis**
   - Visualizes total seats booked across different show times using clean bar charts.

3. **City-Wise Movie Analysis**
   - View all unique cities (sorted alphabetically).
   - Select a city to see top 5 most popular movies.
   - Generates a city-specific comparison chart.

4. **Automatic Date Range Detection**
   - Displays dataset coverage (first date → last date).

5. **Re-analysis Support**
   - Upload another CSV or analyze another city without restarting the app.


## Tech Stack:-
## Tech Stack

| Layer            | Technology   |
|------------------|--------------|
| Backend          | Python       |
| Data Processing  | Pandas       |
| Visualization    | Matplotlib   |
| Frontend         | HTML, CSS    |

## Project Structure


Cinestats/
│
├── backend/
│   ├── main.py              # FastAPI application & routes
│   ├── analysis.py          # Core data analysis & visualization logic
│
├── frontend/
│   └── templates/
│       ├── upload.html      # CSV upload UI
│       ├── index.html       # Main dashboard (show-time analysis)
│       └── city_analysis.html # City-wise analysis page
│
├── data/
│   └── movie_bookings.csv   # Uploaded dataset (auto-updated)
│
├── outputs/
│   └── charts/
│       ├── showtime_popularity.png
│       └── city_top_movies.png
│
├── venv/                    # Virtual environment (gitignored)
├── requirements.txt
└── README.md

## Installation & Setup

### Step-1:Clone the Repository

```bash
git clone https://github.com/your-username/CineStats.git 
cd CineStats
```
### Step-2: Create Virtual Environment
```bash
python -m venv venv
```
#### for Windows :
```bash
venv\Scripts\activate
```
### Step-4: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step-5: Run the project
```bash
python backend/main.py
```
### Step-6: Then open your browser:
```bash
http://127.0.0.1:5000

```

## How It Works (Project Logic)

User uploads a CSV file via the web interface.

File is saved inside the data/ directory.

analysis.py:

Loads the dataset

Computes statistics (total seats, popular show-time, date range)

Generates visualization images

main.py:

Calls analysis functions directly

Passes results to frontend templates

Dashboard renders dynamic insights and charts.

## Dataset Requirements

The CSV file should contain the following columns:

booking_id
movie_name
show_date
show_time
seats_booked
ticket_price
city


## Why This Approach?

Unlike simple Jupyter Notebook analysis:

Separates analysis logic and application logic
Enables real-time user interaction
Makes the project production-ready
Easy to extend (new analytics, new visualizations)

## Future Enhancements

More visualizations (city heatmaps, revenue trends)

CSV validation & error handling

User authentication

Deployment (Docker / Cloud)

## Author

**Md Sahid Raza**  
B.Tech Student  
Rungta College of Engineering and Technology

## License
This project is intended for educational and academic use.