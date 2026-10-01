from fastapi import FastAPI
from routers.users import router as user_router
from routers.products import router as product_router
from routers.orders import router as order_router
from routers.admin import router as admin_router

app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(admin_router)