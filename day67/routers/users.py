import sqlite3
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import get_db

router = APIRouter(prefix="/users",tags=["User"])


class User(BaseModel):
    name: str
    email: str


@router.get("/")
def get_users(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("Select * from users")
    users = cursor.fetchall()

    return {
        "users": users
    }

@router.get("/{user_id}")
def get_users(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("Select * from users where id=?", (user_id,))
    user = cursor.fetchone()
    
    return user

@router.post("/")
def add_user(user: User, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
    )""")

    db.commit()

    name = user.name
    email = user.email

    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    db.commit()

    return {
    "message": "User created successfully"
    }