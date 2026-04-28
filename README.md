\# AI-Powered Smart Attendance \& Identity Management System



\## Overview



This project is an AI-powered multi-mode attendance and identity verification system designed to automate attendance tracking using face recognition technology.



The system supports multiple real-world environments including workplaces, classrooms, events, examinations, and secure access zones.



\---



\## Key Features



\- Face Recognition Attendance System

\- Workplace Attendance Mode

\- Smart Classroom Mode

\- Event Check-in System

\- Exam Identity Verification

\- Secure Access Control

\- Unknown Person Alert System

\- AI Chat Assistant (NLP Based)

\- Voice Assistant Support

\- Interactive Analytics Dashboard

\- Attendance Heatmap Visualization

\- Confidence Accuracy Tracking

\- Automated Report Generation



\---



\## Technologies Used



\- Python

\- OpenCV

\- Face Recognition (dlib)

\- Streamlit

\- SQLite Database

\- Pandas

\- NumPy

\- Seaborn

\- Matplotlib

\- Speech Recognition (Optional)



\---



\## System Modules



1\. Workplace Attendance

2\. Smart Classroom

3\. Event Check-in

4\. Exam Verification

5\. Access Control

6\. Alert System

7\. Analytics Dashboard

8\. AI Chat Assistant

9\. Report Generator

10\. Voice Assistant



\---



\## Installation Guide



Follow the steps below to set up and run the AI Attendance System on your computer.



\---



\### Step 1 — Clone the Repository



Download the project from GitHub.



git clone https://github.com/Shah-Mohsin/AI-Attendance-System.git



cd AI-Attendance-System





\---



\### Step 2 — Create Virtual Environment



Create a virtual environment to manage dependencies.



python -m venv venv





Activate the virtual environment.



Windows:



venv\\Scripts\\activate





\---



\### Step 3 — Install Required Libraries



Install all required packages using the requirements file.



pip install -r requirements.txt





\---



\### Step 4 — Prepare Dataset



Create folders inside:



dataset/





Each folder should be named after a person.



Example:



dataset/

├── Mohsin/

│ ├── 0.jpg

│ ├── 1.jpg

├── Adnan/

│ ├── 0.jpg

├── Faisal/

│ ├── 0.jpg





Each folder must contain face images of that person.



\---



\### Step 5 — Train Face Recognition Model



Run the training script:



python train\_model.py





This will generate:



models/face\_encodings.pkl





\---



\### Step 6 — Run the Main System



Start the main AI system:



python main\_system.py





Available Modes:



\- Workplace Attendance  

\- Smart Classroom  

\- Event Check-in  

\- Exam Verification  

\- Access Control  

\- Alert System  

\- AI Chat Assistant  

\- Report Generator  

\- Voice Assistant  



\---



\### Step 7 — Launch Analytics Dashboard



To open the interactive dashboard:



streamlit run dashboard.py





This will display:



\- Attendance Records  

\- Confidence Metrics  

\- Heatmaps  

\- Trends  

\- Reports  



\---



\### Step 8 — Generate Reports



Run:



python auto\_report.py



reports/





\---



\## System Requirements



\- Python 3.10 or higher  

\- Webcam or external camera  

\- Minimum 4GB RAM  

\- Windows OS recommended  



\---



\## Notes



\- Ensure camera permissions are enabled.

\- Dataset images must be clear and front-facing.

\- Dashboard requires Streamlit to be installed.





