from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# In-memory user store (replace with a real DB for production)
users_db = {}


class AuthRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(data: AuthRequest):
    username = data.username.strip()
    if not username or not data.password:
        return {"error": "Username and password are required"}
    if username in users_db:
        return {"error": "User already exists"}
    users_db[username] = pwd_context.hash(data.password)
    return {"message": "User registered successfully"}


@router.post("/login")
def login(data: AuthRequest):
    username = data.username.strip()
    if username not in users_db:
        return {"error": "Invalid username or password"}
    if not pwd_context.verify(data.password, users_db[username]):
        return {"error": "Invalid username or password"}
    return {"message": "Login successful"}
