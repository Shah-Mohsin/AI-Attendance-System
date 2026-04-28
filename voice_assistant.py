import sqlite3
import pandas as pd
import speech_recognition as sr
import pyttsx3
import re

# =========================
# TEXT TO SPEECH SETUP
# =========================

engine = pyttsx3.init()

def speak(text):

    print(text)

    engine.say(text)

    engine.runAndWait()

# =========================
# LOAD DATABASE
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
# SPEECH RECOGNITION SETUP
# =========================

recognizer = sr.Recognizer()

def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

        try:

            text = recognizer.recognize_google(audio)

            print("You said:", text)

            return text.lower()

        except:

            speak("Sorry, I did not understand.")

            return ""

# =========================
# QUERY HANDLER
# =========================

def process_query(query):

    if "show attendance of" in query:

        match = re.search(
            r"show attendance of (.+)",
            query
        )

        if match:

            name = match.group(1).strip().title()

            df = attendance_df[
                attendance_df["name"] == name
            ]

            if not df.empty:

                speak(
                    f"{name} has {len(df)} attendance records"
                )

            else:

                speak(
                    f"No records found for {name}"
                )

    elif "late employees" in query:

        late_df = attendance_df[
            attendance_df["status"] == "Late"
        ]

        if not late_df.empty:

            names = late_df["name"].tolist()

            speak(
                "Late employees are " +
                ", ".join(names)
            )

        else:

            speak("No late employees")

    elif "attendance trend" in query:

        trend = attendance_df.groupby(
            "date"
        ).size()

        speak("Attendance trend displayed")

        print(trend)

    elif "unknown" in query:

        speak(
            f"Unknown detections count is {len(unknown_df)}"
        )

    elif "total attendance" in query:

        speak(
            f"Total attendance is {len(attendance_df)}"
        )

    elif "exit" in query:

        speak("Exiting voice assistant")

        return False

    else:

        speak(
            "Try saying show attendance of student name"
        )

    return True

# =========================
# MAIN LOOP
# =========================

speak("Voice Assistant Started")

while True:

    query = listen()

    if query == "":
        continue

    result = process_query(query)

    if result == False:
        break