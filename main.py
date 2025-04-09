from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_config import get_db_connection
from starlette.requests import Request


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



conn = get_db_connection()

cursor = conn.cursor()

USER_CREDENTIALS = {'username': 'admin', 'password': 'password123'}


class LoginRequest(BaseModel):
    username: str
    password: str



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/login")
async def login(request: LoginRequest):
    
    username = request.username
    password = request.password

    print(f"Received login request: {request.username}, {request.password}")

    
    if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
        return {"message": "Login successful!"}
    else:
        
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
@app.get("/chat")
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


