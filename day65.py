from fastapi import FastAPI, Query, Depends, Header, Cookie
from pydantic import BaseModel

def pagination(
        page: int = Query(1, gt=0),
        limit: int = Query(10, gt=0, le=100)
): 
    return {
        "page": page,
        "limit": limit
    }

def get_request_id(
        x_request_id: str | None = Header(default= None)
    ):
    return {
        "request_id": x_request_id
    }

def get_request_info(request_id: dict = Depends(get_request_id)):
    return {
        "request_id": request_id["request_id"],
        "source": "api"
    }

def common_parameters(
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0, le=100),
    x_request_id: str | None = Header(default= None)
): 
    return {
        "page": page,
        "limit": limit,
        "request_id": x_request_id
    }

app = FastAPI()

@app.get("/products")
def get_products(common_parameters: dict = Depends(common_parameters)):
    return common_parameters

@app.get("/users")
def get_users(pagination: dict = Depends(pagination)):
    return {
        "endpoints": "users",
        "page": pagination["page"],
        "limit": pagination["limit"]
    }

@app.get("/orders")
def get_orders(common_parameters: dict = Depends(common_parameters)):
    return common_parameters


@app.get("/info")
def get_info(get_request_info: dict = Depends(get_request_info)):
    return get_request_info