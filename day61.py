from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    category: str

class Student(BaseModel):
    name: str
    age: int = Field(ge=18)
    course: str
    marks: float = Field(ge=0, le=100)
    city: str = "kota"

class Employee(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int = Field(ge=18)
    salary: float = Field(ge=0)
    department: str
    experience: int = Field(ge=0)


@app.post("/products")
def add_product(product: Product):
    return product

@app.post("/students")
def add_student(student: Student):
    return {
        "message": "Student added successfully",
        "student": student
    }

@app.post("/employee")
def add_employee(employee: Employee):
    return employee
