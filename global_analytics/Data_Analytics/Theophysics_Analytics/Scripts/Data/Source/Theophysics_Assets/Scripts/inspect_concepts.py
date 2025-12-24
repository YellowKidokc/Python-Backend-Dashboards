import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "08_Database" / "theophysics.db"
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("SELECT concept FROM concepts ORDER BY LENGTH(concept) DESC")
rows = cur.fetchall()
with open("concepts.txt", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(row[0] + "\n")
con.close()

