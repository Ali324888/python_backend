from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator

class UserRegister(BaseModel):
    name: str
    username: str
    email: str
    password: str
    confirm_password: str
    age: int = Field(ge = 18)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("name cannot be empty")

        return value

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        value = value.lower()

        if " " in value:
            raise ValueError("Username cannot contain spaces")
        
        return value

    @field_validator("email")
    @classmethod
    def nomalize_email(cls, value):
        return value.lower()

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, value):
        password_length = len(value)
        if password_length < 8:
            raise ValueError("password minimum 8 characters")
        return value

    @model_validator(mode="after")
    def check_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Password do not match")
        return self



class Product(BaseModel):
    name: str
    price: float = Field(gt = 0)
    quantity: int = Field(gt = 0)
    category: str

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("name cannot be empty")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        value = value.lower()

        if value not in ["electronics", "clothing", "food", "books"]:
            raise ValueError("Category is not valid")

        return value


class Employee(BaseModel):
    name: str
    email: str
    age: int = Field(ge=0)
    salary: float = Field(gt=0)
    confirm_salary: float
    department: str   

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("name cannot be empty")
        return value

    @field_validator("email")
    @classmethod
    def lower_email(cls, value):
        return value.lower()

    @model_validator(mode="after")
    def check_salary(self):
        if self.salary != self.confirm_salary:
            raise ValueError("salary is not same")
        return self

    @field_validator("department")
    @classmethod
    def validate_department(cls, value):
        value = value.lower()
        if value not in ["backend", "frontend", "hr", "finance"]:
            raise ValueError("department not valid")
        return value


app = FastAPI()

@app.post("/register")
def register_user(user: UserRegister):
    return user

@app.post("/product")
def add_product(product: Product):
    return product

@app.post("/employee")
def add_employee(employee: Employee):
    return employee