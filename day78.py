import asyncio
import aiosqlite

async def main():
    async with aiosqlite.connect("notes.db") as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1")
            rows = await cursor.fetchall()
            print(rows)

asyncio.run(main())