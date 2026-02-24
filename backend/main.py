import os
import shutil
from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.analysis import run_analysis, get_all_cities, get_city_movie_details


app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")
# Ensure outputs folder exists (IMPORTANT for Render)
if not os.path.exists("outputs"):
    os.makedirs("outputs")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


# ============================================================
# Main Dashboard Routes
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Display CSV upload page."""
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_csv(request: Request, file: UploadFile = File(...)):
    """Handle CSV upload and run main analysis."""
    os.makedirs("data", exist_ok=True)
    csv_path = "data/movie_bookings.csv"
    
    with open(csv_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    results = run_analysis(csv_path)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "total_seats": results["total_seats"],
            "most_popular_time": results["most_popular_time"],
            "max_seats": results["max_seats"],
            "first_date": results["first_date"],
            "last_date": results["last_date"],
        }
    )


# ============================================================
# City-wise Analysis Routes
# ============================================================

@app.get("/city-analysis", response_class=HTMLResponse)
async def city_analysis_page(request: Request):
    """Display city selection page."""
    try:
        csv_path = "data/movie_bookings.csv"
        cities = get_all_cities(csv_path)
        
        return templates.TemplateResponse(
            "city_analysis.html",
            {
                "request": request,
                "cities": cities,
                "show_results": False
            }
        )
    except FileNotFoundError:
        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "error": "⚠️ Please upload CSV file first!"
            }
        )
    except Exception as e:
        return HTMLResponse(
            content=f"<h2>Error: {str(e)}</h2><a href='/'>Go Back</a>",
            status_code=500
        )


@app.post("/city-analysis", response_class=HTMLResponse)
async def city_analysis_result(request: Request, selected_city: str = Form(...)):
    """Show analysis results for selected city."""
    try:
        csv_path = "data/movie_bookings.csv"
        cities = get_all_cities(csv_path)
        analysis_results = get_city_movie_details(csv_path, selected_city)
        
        return templates.TemplateResponse(
            "city_analysis.html",
            {
                "request": request,
                "cities": cities,
                "selected_city": selected_city,
                "show_results": True,
                "chart_url": analysis_results["chart_url"],
                "top_movies": analysis_results["top_movies"],
                "summary": analysis_results["summary"]
            }
        )
    except Exception as e:
        return HTMLResponse(
            content=f"<h2>Error: {str(e)}</h2><a href='/city-analysis'>Go Back</a>",
            status_code=500
        )


# ============================================================
# Server Startup
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
