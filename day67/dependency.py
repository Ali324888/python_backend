from fastapi import Header, HTTPException


def check_api_key(
    x_api_key: str | None = Header(default=None)
):
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API key required"
        )

    return x_api_key