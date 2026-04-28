import sqlite3

print("Creating unknown_log table...")

conn = sqlite3.connect("database/attendance.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS unknown_log (
    date TEXT,
    time TEXT
)
""")

conn.commit()

conn.close()

print("unknown_log table created successfully.")