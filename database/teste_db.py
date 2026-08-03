import sqlite3
from database.database import DATABASE

print("Banco:", DATABASE)

conn = sqlite3.connect(str(DATABASE))

cursor = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

print(cursor.fetchall())

conn.close()