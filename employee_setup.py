import sqlite3

conn = sqlite3.connect("database/employees.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT,
    name TEXT,
    department TEXT,
    shift_start TEXT
)
""")

employees = [

("EMP001","Mohsin","IT","09:00"),
("EMP002","Adnan","HR","09:00"),
("EMP003","Faisal","Finance","09:30"),
("EMP004","Khubiab","Security","08:30")

]

cursor.executemany(
"INSERT INTO employees VALUES (?,?,?,?)",
employees
)

conn.commit()

conn.close()

print("Employee database created.")