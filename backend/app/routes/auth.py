from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# Import database functions
from app.database import check_user, insert_user, valid_login

# Create router for authentication routes
router = APIRouter()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="frontend/templates")


# ===== REGISTER ROUTES =====

@router.get("/register")
def get_register_page(request: Request):
    """
    GET /register - Shows the registration form.
    """
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def post_register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    confirm_password: str = Form(...)
):
    """
    POST /register - Handles registration form submission.
    
    Form fields:
    - username: User's chosen username
    - password: User's password (not hashed yet, I will do that later)
    - email: User's email (collected but not saved to DB yet)
    - confirm_password: Password confirmation (validated client side)
    """
    # Check if username already exists
    if check_user(username):
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "username_taken": True}
        )
    
    # Create new user
    insert_user(username, email, password)
    
    # Redirect to login page after successful registration
    return RedirectResponse(url="/login", status_code=303)


# ===== LOGIN ROUTES =====

@router.get("/login")
def get_login_page(request: Request):
    """
    GET /login - Shows the login form.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def post_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """
    POST /login - Handles login form submission.
    
    Form fields:
    - username: User's username
    - password: User's password
    """
    # Validate credentials
    if not valid_login(username, password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "login_failed": True}
        )
    
    # Successful login so redirect to home page
    # TODO: Add session management later for logout 
    return RedirectResponse(url="/pdf2quizhome", status_code=303)


# ===== HOME PAGE =====

@router.get("/pdf2quizhome")
def get_home(request: Request):
    """
    GET /pdf2quizhome - Shows the main application page.
    This is where users can upload PDFs after logging in.
    """
    return templates.TemplateResponse("pdf2quizhome.html", {"request": request})


# ===== LOGOUT =====

@router.get("/logout")
def logout():
    """
    GET /logout - Logs out user and redirects to login.
    Currently just redirects because no session clearing yet.
    TODO: Add session management.
    """
    return RedirectResponse(url="/login", status_code=303)