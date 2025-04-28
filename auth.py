from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from models import LoginRequest, RegisterRequest
from database import Database
import bcrypt

# Initialize router
router = APIRouter()

# Initialize templates
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/login")
async def login(request: LoginRequest):
    username = request.username
    password = request.password.encode('utf-8')
    
    if Database.check_user_credentials(username, password):
        # Return username along with success message
        return {"message": "Login successful!", "username": username}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")

@router.post("/register")
async def register_user(request: RegisterRequest):
    email = request.email
    username = request.username
    password = request.password
    confirm_password = request.confirm_password 

    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    
    # Hash the password
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    
    # Register the user
    error = Database.register_user(email, username, hashed_password)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return {"message": "Registration successful", "username": username} 