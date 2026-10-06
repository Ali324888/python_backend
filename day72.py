import jwt
from jwt.exceptions import InvalidTokenError

from pwdlib import PasswordHash
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

password_hash = PasswordHash.recommended()

app = FastAPI()

fake_db = {}

SECRET_KEY = "my-super-secret-key-for-fastapi-jwt-12345"
ALGORITHM = "HS256"


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload

class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/register")
def registration(data: RegisterRequest):
    hashed_password = password_hash.hash(data.password)
    email = data.email

    if data.email in fake_db:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    fake_db[email] = {
        "id": len(fake_db)+1,
        "email": email,
        "password": hashed_password
    }

    return {
        "message": "User registered successfully"
    }

@app.post("/login")
def login(data: LoginRequest):
    email = data.email
    password = data.password

    user = fake_db.get(email)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail= "Invalid email or password"
        )
    is_valid_password = password_hash.verify(password, user["password"])

    if not is_valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    payload = {
        "sub": str(user["id"]),
        "email": user["email"]
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/profile")
def get_profile(user = Depends(get_current_user)):
    return {
        "message": "Welcome to profile",
        "user": user
    }