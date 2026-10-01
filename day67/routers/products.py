import sqlite3
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import get_db

router = APIRouter(prefix="/products",tags=["Product"])


class Product(BaseModel):
    name: str
    price: float
    quantity: int


@router.get("/")
def get_users(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("Select * from products")
    products = cursor.fetchall()

    return {
        "products": products
    }

@router.get("/{product_id}")
def get_users(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("Select * from products where id=?", (product_id,))
    product = cursor.fetchone()
    
    return product

@router.post("/")
def add_user(product: Product, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
    )""")

    db.commit()

    name = product.name
    price = product.price
    quantity = product.quantity

    cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
    db.commit()

    return {
    "message": "product added successfully"
    }