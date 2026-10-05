from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

app = FastAPI()

class ProductNotFoundError(Exception):
    def __init__(self, product_id):
        self.product_id = product_id


@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundError 
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": {
                "code": "PRODUCT_NOT_FOUND",
                "message": f"Product {exc.product_id} not found"
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_handler(
    requset: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code= 422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors()
            }
        }
    )

class Employee(BaseModel):
    name: str
    age: int = Field(ge=18)
    salary: float = Field(gt=0)

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 0:
        raise HTTPException(
            status_code= 400,
            detail="User not found!"
        )
    elif user_id == 1:
        return {
            "id": user_id,
            "name": "adil"
        }
    else:
        raise HTTPException(
            status_code= 404,
            detail="User not found!"
        )

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id == 1:
        return {
            "name": "TV",
            "price": 250
        }
    else:
        raise ProductNotFoundError(product_id)

@app.post("/employee")
def get_employee(employee: Employee):
    return employee