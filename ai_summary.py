import sqlite3
import pandas as pd

conn = sqlite3.connect("database/attendance.db")

df = pd.read_sql_query(
    "SELECT * FROM attendance",
    conn
)

conn.close()

print("\nAI Attendance Intelligence Report\n")

if df.empty:

    print("No attendance data.")

else:

    total = len(df)

    unique_people = df["name"].nunique()

    most_present = df["name"].value_counts().idxmax()

    daily_counts = df.groupby("date").size()

    busiest_day = daily_counts.idxmax()

    print("Total Records:", total)

    print("Unique People:", unique_people)

    print("Most Frequent:", most_present)

    print("Busiest Day:", busiest_day)