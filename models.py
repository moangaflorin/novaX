from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str

class ChatMessage(BaseModel):
    sender: str
    text: str
    timestamp: Optional[datetime] = None
    room_id: str = "general" 