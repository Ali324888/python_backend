import sqlite3
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import get_db

router = APIRouter(prefix="/orders",tags=["Order"])


class order(BaseModel):
    name: str


@router.get("/")
def get_orders(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("Select * from orders")
    orders = cursor.fetchall()

    return {
        "orders": orders
    }

@router.get("/{order_id}")
def get_orders(order_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("Select * from orders where id=?", (order_id,))
    order = cursor.fetchone()
    
    return order

@router.post("/")
def add_order(order: order, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    )""")

    db.commit()

    name = order.name

    cursor.execute("INSERT INTO orders (name) VALUES (?)",(name,))
    db.commit()

    return {
    "message": "order created successfully"
    }