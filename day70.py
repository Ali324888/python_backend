from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

security = HTTPBearer()

class LoginRequest(BaseModel):
    email: str
    password: str

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    return {
        "token": token
    }


app = FastAPI()

@app.post("/login")
def login(data: LoginRequest):

    if(data.email == "adil@example.com" and data.password == "12345"):
        return {
            "message": "Login successful"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )

@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return {
        "message": "Welcome to profile",
        "user": user
    }