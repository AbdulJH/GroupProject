from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Import routers
from app.routes import auth

# Import database initialization
from app.database import create_users_table

# Create FastAPI application
app = FastAPI(
    title="PDF2Quiz",
    version="1.0.0",
    description="Convert PDF documents into quizzes using AI"
)

# Include authentication routes (register, login, logout, etc.)
app.include_router(auth.router)

# Mount static files (CSS, JavaScript, images)
# Files in frontend/static/ will be served at /static/
# Small note: name="static" allows url_for('static', ...) to work in templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.on_event("startup")
def startup_event():
    """
    Runs once when the application starts up.
    Creates database tables if they don't exist.
    """
    print("Starting up PDF2Quiz application...")
    create_users_table()
    print("Database tables created/verified")


@app.get("/")
def read_root():
    """
    Root endpoint - redirects visitors to the login page.
    """
    return RedirectResponse(url="/login")


