from fastapi import FastAPI, Path, Query, Header, Cookie
from pydantic import BaseModel

app = FastAPI()

@app.get("/products")
def create_product(
        category: str | None = None,
        min_price: float | None = Query(gt=0),
        max_price: float  | None = Query(gt=1),
        limit: int = Query(default=1, ge=1, le=100)
):
    return {
    "category": category,
    "min_price": min_price,
    "max_price": max_price,
    "limit": limit
    }

@app.get("/users/{user_id}/orders")
def get_users(
    user_id: int = Path(gt=0),
    page: int = Query(ge=1),
    limit: int = Query(gt=0, le=100)
):
    return {
        "user_id": user_id,
        "page": page,
        "limit": limit
    }

@app.get("/profile")
def get_profile(
    user_agent: str |None = Header(default=None),
    Authorization: str | None = Header(default=None),
    session_id: str | None = Cookie(default=None)
):
    return    {
        "user_agent": user_agent,
        "authorization": Authorization,
        "session_id": session_id
    }

@app.get("/products/{category}")
def get_products(
  category: str = Path(min_length=2),
  max_price: float = Query(gt=0),      
  min_price: float = Query(gt=0),     
  page: int = Query(ge=1),
  limit: int = Query(gt=0, le=100),
  x_request_id: str = Header(default=None),
  session_id: str = Cookie(default=None)
):
    return {
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "page": page,
        "limit": limit,
        "request_id": x_request_id,
        "session_id": session_id
    }