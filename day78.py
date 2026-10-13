import asyncio
import aiosqlite

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager


async def init_db():
    async with aiosqlite.connect("tasks.db") as db:
         await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)
         await db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
     await init_db()
     yield

app = FastAPI(lifespan=lifespan)

async def get_db():
     async with aiosqlite.connect("tasks.db") as db:
          db.row_factory = aiosqlite.Row
          yield db


class Task(BaseModel):
     title: str

class UpdateTask(BaseModel):
     title: str | None = None
     completed: bool | None = None


@app.post("/tasks", status_code=201)
async def create_task(data: Task, db: aiosqlite.Connection = Depends(get_db)):
     async with db.execute("INSERT INTO tasks (title) VALUES (?)",(data.title, ),) as cursor:
          task_id = cursor.lastrowid

          await db.commit()

          return {
               "id" : task_id,
               "title": data.title,
               "completed": False
          }

@app.get("/tasks")
async def get_all_tasks(db: aiosqlite.Connection = Depends(get_db)):
     async with db.execute("SELECT * FROM tasks") as cursor:
          rows = await cursor.fetchall()

          return [
               {
                    "id": row["id"],
                    "title": row["title"],
                    "completed": row["completed"],
               }
               for row in rows
          ]

@app.get("/tasks/{task_id}")
async def get_all_tasks(task_id: int, db: aiosqlite.Connection = Depends(get_db)):
     async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
          row = await cursor.fetchone()

          if row is None:
               raise HTTPException(status_code=404, detail="Task not found")
          

          return {
                    "id": row["id"],
                    "title": row["title"],
                    "completed": row["completed"],
               }

@app.patch("/tasks/{task_id}")
async def get_all_tasks(task_id: int, data: UpdateTask, db: aiosqlite.Connection = Depends(get_db)):
     changes = data.model_dump(exclude_unset=True)

     if not changes:
          raise HTTPException(
               status_code=400,
               detail="No fileds provided"
          )

     async with db.execute("Select * from tasks where id=?", (task_id,)) as cursor:
          row = await cursor.fetchone()

     if row is None:
          raise HTTPException(
               status_code=404,
               detail="Task not found"
          )
     if "title" in changes and changes["title"] is None:
          raise HTTPException(
               status_code=400,
               detail="title cannot be null"
          )
     print(changes)
     if "completed" in changes and changes["completed"] is None:
          raise HTTPException(
               status_code=400,
               detail="completed cannot be null"
          )

     await db.execute("Update tasks Set title=?, completed=? where id=?", (data.title, int(data.completed), task_id))
     await db.commit()

     return {"message": "Task Updated"}

@app.delete("/tasks/{task_id}")
async def get_all_tasks(task_id: int, db: aiosqlite.Connection = Depends(get_db)):
     async with db.execute("DELETE FROM tasks WHERE id=?", (task_id,)) as cursor:
          deleted = cursor.rowcount
     await db.commit()

     if deleted is None:
          raise HTTPException(
               status_code=404,
               detail="Task not found"
          )
     
     return {"message": "Task deleted"}

@app.post("tasks/transactions")
async def transaction_demo(db: aiosqlite.Connection = Depends(get_db)):
     try:
          await db.execute("INSERT INTO tasks (title) VALUES (?)",
            ("First task",),)

          await db.execute("INSERT INTO pasks (title) VALUES (?)",
                      ("First task",),)
          await db.commit()

     except aiosqlite.Error:
          await db.rollback()
          raise HTTPException(
               status_code=500,
               detail="Db operation failed"
          )

     return {"message": "Transaction completed"}

async def count_tasks():
    async with aiosqlite.connect("tasks.db") as db:
        async with db.execute(
            "SELECT COUNT(*) FROM tasks"
        ) as cursor:
            row = await cursor.fetchone()
            return row[0]


async def count_pending_tasks():
    async with aiosqlite.connect("tasks.db") as db:
        async with db.execute(
            "SELECT COUNT(*) FROM tasks WHERE completed = 0"
        ) as cursor:
            row = await cursor.fetchone()
            return row[0]


@app.get("/dashboard")
async def dashboard():
    total, pending = await asyncio.gather(
        count_tasks(),
        count_pending_tasks(),
    )

    return {
        "total_tasks": total,
        "pending_tasks": pending,
    }