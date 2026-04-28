import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Attendance Dashboard",
    layout="wide",
    page_icon="📊"
)

st.title("📊 AI Attendance Analytics Dashboard")

# =========================================
# LOAD DATABASE
# =========================================

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

# =========================================
# SAFETY CHECK
# =========================================

if attendance_df.empty:

    st.warning("No attendance data available.")
    st.stop()

# =========================================
# FILTER SIDEBAR
# =========================================

st.sidebar.header("🔎 Filters")

names = st.sidebar.multiselect(
    "Select Person",
    options=attendance_df["name"].unique(),
    default=attendance_df["name"].unique()
)

dates = st.sidebar.multiselect(
    "Select Date",
    options=attendance_df["date"].unique(),
    default=attendance_df["date"].unique()
)

filtered_df = attendance_df[
    (attendance_df["name"].isin(names)) &
    (attendance_df["date"].isin(dates))
]

# =========================================
# KPI CARDS
# =========================================

total_records = len(filtered_df)

unique_people = filtered_df["name"].nunique()

unknown_count = len(unknown_df)

avg_conf = (
    filtered_df["confidence"].mean()
    if "confidence" in filtered_df.columns
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    total_records
)

col2.metric(
    "Unique People",
    unique_people
)

col3.metric(
    "Unknown Detections",
    unknown_count
)

col4.metric(
    "Avg Confidence",
    f"{avg_conf:.2f}%"
)

st.divider()

# =========================================
# ATTENDANCE TABLE
# =========================================

st.subheader("📋 Attendance Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=300
)

st.divider()

# =========================================
# ATTENDANCE COUNT BAR CHART
# =========================================

st.subheader("📊 Attendance Count Per Person")

count_data = filtered_df["name"].value_counts()

st.bar_chart(count_data)

st.divider()

# =========================================
# DAILY TREND
# =========================================

st.subheader("📈 Daily Attendance Trend")

daily_data = filtered_df.groupby(
    "date"
).size()

st.line_chart(daily_data)

st.divider()

# =========================================
# CONFIDENCE HISTOGRAM
# =========================================

if "confidence" in filtered_df.columns:

    st.subheader("🎯 Confidence Distribution")

    fig1, ax1 = plt.subplots()

    sns.histplot(
        filtered_df["confidence"],
        bins=10,
        kde=True,
        ax=ax1
    )

    st.pyplot(fig1)

st.divider()

# =========================================
# HEATMAP
# =========================================

st.subheader("🔥 Attendance Heatmap")

heatmap_data = pd.pivot_table(
    filtered_df,
    values="time",
    index="name",
    columns="date",
    aggfunc="count",
    fill_value=0
)

fig2, ax2 = plt.subplots(
    figsize=(10,5)
)

sns.heatmap(
    heatmap_data,
    cmap="YlGnBu",
    annot=True,
    fmt="d",
    linewidths=0.5,
    ax=ax2
)

st.pyplot(fig2)

st.divider()

# =========================================
# LATE EMPLOYEES
# =========================================

if "status" in filtered_df.columns:

    st.subheader("⏰ Late Employees")

    late_df = filtered_df[
        filtered_df["status"] == "Late"
    ]

    if not late_df.empty:

        st.dataframe(
            late_df,
            use_container_width=True
        )

    else:

        st.success("No Late Employees")

st.divider()

# =========================================
# CONFIDENCE BOX PLOT
# =========================================

if "confidence" in filtered_df.columns:

    st.subheader("📦 Confidence Spread")

    fig3, ax3 = plt.subplots()

    sns.boxplot(
        x=filtered_df["confidence"],
        ax=ax3
    )

    st.pyplot(fig3)

st.divider()

# =========================================
# UNKNOWN ALERT VISUALIZATION
# =========================================

st.subheader("⚠ Unknown Detection Overview")

unknown_counts = unknown_df.groupby(
    "date"
).size()

if not unknown_counts.empty:

    st.bar_chart(unknown_counts)

else:

    st.info("No Unknown Records Yet")

st.divider()

# =========================================
# SUMMARY SECTION
# =========================================

st.subheader("📌 System Summary")

st.info(
"""
✔ Face Recognition Active  
✔ Attendance Tracking Enabled  
✔ Analytics Dashboard Running  
✔ AI Accuracy Monitoring Active  
"""
)