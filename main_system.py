import subprocess
import os
import time

# =========================================
# VENV PYTHON PATH
# =========================================

PYTHON_PATH = r"venv\Scripts\python.exe"

# =========================================
# CLEAR SCREEN
# =========================================

def clear_screen():
    os.system("cls")

# =========================================
# RUN SCRIPT FUNCTION
# =========================================

def run_script(script_name):

    try:

        print(f"\nStarting {script_name}...\n")

        subprocess.run(
            [PYTHON_PATH, script_name],
            check=False
        )

    except Exception as e:

        print("Error running:", script_name)

        print(e)

# =========================================
# RUN DASHBOARD
# =========================================

def run_dashboard():

    try:

        subprocess.run(
            ["streamlit", "run", "dashboard.py"],
            check=False
        )

    except Exception as e:

        print("Dashboard error:", e)

# =========================================
# WAIT FUNCTION
# =========================================

def wait_return():

    input("\nPress ENTER to return to main menu...")

# =========================================
# MAIN LOOP
# =========================================

while True:

    clear_screen()

    print("\n==============================")
    print("   AI Attendance System Hub")
    print("==============================\n")

    print("1  - Workplace Attendance")
    print("2  - Smart Classroom")
    print("3  - Event Check-in")
    print("4  - Exam Verification")
    print("5  - Access Control")
    print("6  - AI Alert System")
    print("7  - Analytics Dashboard")
    print("8  - AI Chat Assistant")
    print("9  - Generate Report")
    print("10 - Voice AI Assistant")
    print("0  - Exit")

    choice = input("\nEnter your choice: ").strip()

    # =====================================

    if choice == "1":

        run_script("recognize.py")
        wait_return()

    elif choice == "2":

        run_script("classroom_mode.py")
        wait_return()

    elif choice == "3":

        run_script("event_checkin.py")
        wait_return()

    elif choice == "4":

        run_script("exam_verification.py")
        wait_return()

    elif choice == "5":

        run_script("access_control.py")
        wait_return()

    elif choice == "6":

        run_script("alert_system.py")
        wait_return()

    elif choice == "7":

        run_dashboard()
        wait_return()

    elif choice == "8":

        run_script("ai_chat.py")
        wait_return()

    elif choice == "9":

        run_script("auto_report.py")
        wait_return()

    elif choice == "10":

        run_script("voice_assistant.py")
        wait_return()

    elif choice == "0":

        print("\nExiting System...")
        break

    else:

        print("\nInvalid choice.")
        time.sleep(2)