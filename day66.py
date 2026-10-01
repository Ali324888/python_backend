import sqlite3
from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel

def get_db():
    conn = sqlite3.connect("app.db", check_same_thread=False)

    try:
        yield conn
    finally:
        conn.close()

def get_user_by_db(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(
        status_code=404,
        detail="User not found"
    )
    
    return {
        "id": result[0],
        "name": result[1],
        "email": result[2]
    }

def pagination(page: int = Query(1,gt=0), 
               limit: int = Query(10, gt=0, le=100)):
    return {
        "page": page,
        "limit": limit
    }

app = FastAPI()


class User(BaseModel):
    name: str
    email: str

@app.get("/health/db")
def database_health(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT 1")
    result = cursor.fetchone()

    return result

@app.post("/users")
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

@app.get("/users")
def get_user(db: sqlite3.Connection = Depends(get_db)):

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")

    result = cursor.fetchall()

    users = []

    for item in result:
        users.append({
            "id": item[0],
            "name": item[1],
            "email": item[2]
        })

    return {
        "users": users
    }

@app.get("/users/{user_id}")
def get_user_by_id(user = Depends(get_user_by_db)):
    return user

@app.get("/users")
def get_users(db: sqlite3.Connection = Depends(get_db), params = Depends(pagination)):
    offset = (params["page"] - 1) * params["limit"]
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email FROM users LIMIT ? OFFSET ?", (params["limit"], offset))

    result = cursor.fetchall()

    users = []
    
    for item in result:
        users.append({
            "id": item[0],
            "name": item[1],
            "email": item[2]
        })
    
    return {
        "users": users
    }