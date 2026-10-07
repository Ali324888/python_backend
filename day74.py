import jwt
from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError

app = FastAPI()
# security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

fake_db = {}

SECRET_KEY = "my-super-secret-key-for-fastapi-jwt-12345"
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str


def find_user_by_id(user_id: int):
    for user in fake_db.values():
        if user["id"] == user_id:
            return user


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

    token_type = payload.get("type")

    if token_type != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

    user_id  = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

    return payload


def create_access_token(user_id:int, email: str):
    expire_time = datetime.now(timezone.utc)+ timedelta(minutes=15)
    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "access",
        "exp": expire_time
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id:int):
    expire_time = datetime.now(timezone.utc)+ timedelta(days=7)
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire_time
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/refresh")
def refresh_token(data: RefreshRequest):
    try:
        token = data.refresh_token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user = find_user_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return {
        "access_token": create_access_token(user["id"], user["email"]),
        "token_type": "bearer"
    }






@app.post("/register")
def registeration(data: RegisterRequest):
    email = data.email
    password = data.password

    if email in fake_db:
        raise HTTPException(
            status_code=409,
            detail="User already exist"
        )

    hashed_password = password_hash.hash(password)

    fake_db[email] = {
        "id": len(fake_db)+1,
        "email": email, 
        "password": hashed_password
    }

    return {
        "message": "User register successfully"
    }

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    user = fake_db.get(email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    valid_password = password_hash.verify(password, user["password"])

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user["id"], user["email"])
    refresh_token = create_refresh_token(user["id"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.get("/profile")
def get_profile(user = Depends(get_current_user)):
    return {
        "message": "Welcome to profile",
        "user": user
    }