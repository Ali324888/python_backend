from fastapi import FastAPI
from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    state: str
    pincode: int


class Student(BaseModel):
    name: str
    age: int
    course: str
    address: Address


class Product(BaseModel):
    name: str
    price: float = Field(gt = 0)
    quantity: int = Field(gt = 0)

class Order(BaseModel):
    customer_name: str
    products: list[Product]


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    address: Address




app = FastAPI()

@app.post("/students")
def create_student(student: Student):
    return student

@app.post("/order")
def create_order(order: Order):
    return order

@app.post("/users")
def create_user(user: UserCreate):
    return user

@app.get("/users/1", response_model=UserResponse)
def get_user():
    user = {
            "id": 1,
            "name": "Adil",
            "email": "adil@example.com",
            "password": "secret123",
            "role": "admin",
            "address": {
                    "city": "Kota",
                    "state": "Rajasthan",
                    "pincode": 324005
                } 
        }
    return user