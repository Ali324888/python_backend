import time, uuid
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def logging_middleware(request: Request, call_next):

    print("Method: ", request.method)
    print("Path: ", request.url.path)

    response = await call_next(request)

    print("response status: ", response.status_code)

    return response

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    process_time = end_time - start_time
    print("Process time: ", process_time)
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    print("Request ID: ", request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

@app.get("/users")
def get_users():
    print("endpoint chala hai")
    return "all users"

