import sqlite3
import pandas as pd
import re

print("\n==============================")
print("   AI Attendance Assistant")
print("==============================\n")

# =========================
# LOAD ATTENDANCE DATA
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
# LOAD EMPLOYEE DATA
# =========================

emp_conn = sqlite3.connect("database/employees.db")

employee_df = pd.read_sql_query(
    "SELECT * FROM employees",
    emp_conn
)

emp_conn.close()

# Merge data

merged_df = pd.merge(
    attendance_df,
    employee_df,
    on="name",
    how="left"
)

# =========================
# SHOW HELP
# =========================

print("You can ask queries like:\n")

print("Show attendance of <student name>")
print("Show late employees")
print("Attendance trend")
print("Show attendance today")
print("Show attendance of department <department name>")
print("Unknown detections")
print("Total attendance")
print("Unique people")

# =========================
# CHAT LOOP
# =========================

while True:

    query = input("\nAsk: ").strip()

    query_lower = query.lower()

    if query_lower == "exit":

        print("Closing AI Assistant...")
        break

    # =========================================
    # SHOW ATTENDANCE OF ANY STUDENT
    # =========================================

    elif "show attendance of" in query_lower:

        # Extract name dynamically

        name_match = re.search(
            r"show attendance of (.+)",
            query_lower
        )

        if name_match:

            name = name_match.group(1).strip().title()

            person_df = merged_df[
                merged_df["name"] == name
            ]

            if not person_df.empty:

                print(f"\nAttendance of {name}:\n")

                print(
                    person_df[
                        ["name","date","time","status"]
                    ]
                )

            else:

                print(
                    f"No attendance records found for {name}"
                )

        else:

            print("Please specify student name.")

    # =========================================
    # SHOW LATE EMPLOYEES
    # =========================================

    elif "late employees" in query_lower:

        late_df = merged_df[
            merged_df["status"] == "Late"
        ]

        if not late_df.empty:

            print("\nLate Employees:\n")

            print(
                late_df[
                    ["name","date","time"]
                ]
            )

        else:

            print("No late employees found.")

    # =========================================
    # ATTENDANCE TREND
    # =========================================

    elif "attendance trend" in query_lower:

        if not merged_df.empty:

            trend = merged_df.groupby(
                "date"
            ).size()

            print("\nAttendance Trend:\n")

            print(trend)

        else:

            print("No attendance data available.")

    # =========================================
    # SHOW TODAY ATTENDANCE
    # =========================================

    elif "today" in query_lower:

        if not merged_df.empty:

            latest_date = merged_df[
                "date"
            ].iloc[-1]

            today_df = merged_df[
                merged_df["date"] == latest_date
            ]

            print("\nToday's Attendance:\n")

            print(today_df)

        else:

            print("No attendance recorded today.")

    # =========================================
    # SHOW DEPARTMENT ATTENDANCE
    # =========================================

    elif "department" in query_lower:

        dept_match = re.search(
            r"department (.+)",
            query_lower
        )

        if dept_match:

            dept = dept_match.group(1).strip().upper()

            dept_df = merged_df[
                merged_df["department"] == dept
            ]

            if not dept_df.empty:

                print(f"\nAttendance of Department {dept}:\n")

                print(dept_df)

            else:

                print(
                    f"No attendance found for department {dept}"
                )

        else:

            print("Specify department name.")

    # =========================================
    # UNKNOWN DETECTIONS
    # =========================================

    elif "unknown" in query_lower:

        print(
            "\nUnknown detections:",
            len(unknown_df)
        )

    # =========================================
    # TOTAL ATTENDANCE
    # =========================================

    elif "total" in query_lower:

        print(
            "\nTotal attendance records:",
            len(merged_df)
        )

    # =========================================
    # UNIQUE PEOPLE
    # =========================================

    elif "unique" in query_lower:

        print(
            "\nUnique people:",
            merged_df["name"].nunique()
        )

    # =========================================
    # UNKNOWN QUERY
    # =========================================

    else:

        print("\nTry queries like:\n")

        print("Show attendance of Adnan")
        print("Show attendance of Ruhan")
        print("Show late employees")
        print("Attendance trend")
        print("Show attendance today")
        print("Show attendance of department IT")
        print("Unknown detections")
        print("Total attendance")
        print("Unique people")
        print("Type 'exit' to quit")