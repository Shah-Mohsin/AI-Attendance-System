import sqlite3
import pandas as pd
import os

print("\nGenerating Reports...\n")

os.makedirs("reports", exist_ok=True)

# =========================
# ATTENDANCE REPORT
# =========================

conn = sqlite3.connect("database/attendance.db")

attendance_df = pd.read_sql_query(
    "SELECT * FROM attendance",
    conn
)

unknown_df = pd.read_sql_query(
    "SELECT * FROM unknown_log",
    conn
)

conn.close()

# =========================
# EVENT REPORT
# =========================

try:

    event_conn = sqlite3.connect("database/events.db")

    event_df = pd.read_sql_query(
        "SELECT * FROM event_checkin",
        event_conn
    )

    event_conn.close()

except:

    event_df = pd.DataFrame()

# =========================
# SAVE REPORTS
# =========================

attendance_file = "reports/attendance_report.csv"
unknown_file = "reports/unknown_report.csv"
event_file = "reports/event_report.csv"

attendance_df.to_csv(
    attendance_file,
    index=False
)

unknown_df.to_csv(
    unknown_file,
    index=False
)

if not event_df.empty:

    event_df.to_csv(
        event_file,
        index=False
    )

# =========================
# SUMMARY
# =========================

print("Reports Generated:\n")

print(attendance_file)
print(unknown_file)

if not event_df.empty:
    print(event_file)

print("\nSummary:")

print(
"Total Attendance:",
len(attendance_df)
)

print(
"Unknown Detections:",
len(unknown_df)
)

if not event_df.empty:
    print(
    "Event Records:",
    len(event_df)
    )