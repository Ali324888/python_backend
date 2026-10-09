import asyncio

async def task_one():
    print("Task 1 started")
    await asyncio.sleep(2)
    print("Task 1 completed")
    return "Result 1"


async def task_two():
    print("Task 2 started")
    await asyncio.sleep(3)
    print("Task 2 completed")
    return "Result 2"

async def main():
    task1 = asyncio.create_task(task_one())
    task2 = asyncio.create_task(task_two())

    result1 = await task1
    result2 = await task2

    print(result1)
    print(result2)


# asyncio.run(main())

async def slow_api():
    await asyncio.sleep(5)
    return "API response"

async def main1():
    try:
        result = await asyncio.wait_for(slow_api(), timeout=2)
        print(result)
    except asyncio.TimeoutError:
        print("Task timed out")

# asyncio.run(main1())

async def long_running_task():
    try:
        print("Task started")
        await asyncio.sleep(10)
        print("Task completed")

    except asyncio.CancelledError:
        print("Task cancelled")
        raise

async def main2():
    try: 
        task3 = asyncio.create_task(long_running_task())
        await asyncio.sleep(2)
        task3.cancel()

    except asyncio.CancelledError:
        print("Task was canceled")


asyncio.run(main2())