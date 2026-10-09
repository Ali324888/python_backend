import asyncio
from fastapi import FastAPI

app = FastAPI()

# async def hello():
#     print("Hello")
#     await asyncio.sleep(5)
#     print("World")

# asyncio.run(hello())

async def task_one():
    print("task 1 started")
    await asyncio.sleep(2)
    print("task 1 completed")

async def task_two():
    print("task 2 started")
    await asyncio.sleep(2)
    print("task 2 completed")

async def main1():
    await task_one()
    await task_two()

async def main2():
    await asyncio.gather(task_one(), task_two())

# asyncio.run(main1())
# asyncio.run(main2())

async def fetch_data():
    await asyncio.sleep(2)

    return {
        "message": "Data fetched"
    }

async def fetch_profile():
    await asyncio.sleep(2)

    return {
        "name": "Adil"
    }


async def fetch_notifications():
    await asyncio.sleep(2)

    return [
        "New message",
        "New login"
    ]

@app.get("/async-data")
async def async_data():
    result = await fetch_data()
    return result


@app.get("/dashboard")
async def get_dashboard():
    profile, notifications = await asyncio.gather(
        fetch_profile(),
        fetch_notifications()
    )

    return {
        "profile": profile,
        "notifications": notifications
    }