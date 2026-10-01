import sqlite3

def get_db():
    conn = sqlite3.connect("./app.db", check_same_thread=False)

    try:
        yield conn
    finally:
        conn.close()