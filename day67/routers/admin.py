from fastapi import APIRouter, Depends

from dependency import check_api_key


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(check_api_key)]
)


@router.get("/users")
def get_admin_users():
    return {
        "message": "Admin users data"
    }


@router.get("/orders")
def get_admin_orders():
    return {
        "message": "Admin orders data"
    }


@router.get("/reports")
def get_admin_reports():
    return {
        "message": "Admin reports data"
    }