from pwdlib import PasswordHash
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

password_hash = PasswordHash.recommended()

app = FastAPI()

password = '12345'

hashed_password = password_hash.hash(password)

print("Hashed password: ", hashed_password)

print("Correct password: ",password_hash.verify(password, hashed_password))
print("Wrong password: ",password_hash.verify('123', hashed_password))

fake_db = {}

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
    print(user)
    is_valid_password = password_hash.verify(data.password, user["password"])
    print(is_valid_password)

    if not is_valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful"
    }