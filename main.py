from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from db_config import get_db_connection
from starlette.requests import Request
import bcrypt


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



class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/login")
async def login(request: LoginRequest):
    
    username = request.username
    password = request.password.encode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))

    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    stored_hash = bytes.fromhex(result[0][2:])

    if bcrypt.checkpw(password, stored_hash):
        return {"message": "Login succsessful!"}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
        
@app.get("/chat")
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/register")
async def register_user(request: RegisterRequest):
    email = request.email
    username = request.username
    password = request.password
    confirm_password = request.confirm_password 

    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM public.users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Email already in use.")
    
    cursor.execute("SELECT 1 FROM public.users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Username already taken.")
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)

    cursor.execute(
        "INSERT INTO public.users (email, username, password) VALUES (%s, %s, %s)",
        (email, username, hashed_password)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Registration successful"}
