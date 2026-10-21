import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Student Performance Analysis System
# Single-file Streamlit web application
# ---------------------------------------------------------

st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

# Built-in sample dataset: everything is kept in this file.
SAMPLE_DATA = [
    {"Student Name": "Aarav", "Maths": 86, "Science": 91, "English": 78, "Attendance (%)": 94},
    {"Student Name": "Diya", "Maths": 92, "Science": 88, "English": 95, "Attendance (%)": 98},
    {"Student Name": "Rahul", "Maths": 67, "Science": 73, "English": 70, "Attendance (%)": 82},
    {"Student Name": "Sneha", "Maths": 45, "Science": 58, "English": 62, "Attendance (%)": 76},
    {"Student Name": "Arjun", "Maths": 74, "Science": 81, "English": 69, "Attendance (%)": 88},
    {"Student Name": "Meera", "Maths": 38, "Science": 49, "English": 55, "Attendance (%)": 65},
]

PASS_MARK = 40
SUBJECTS = ["Maths", "Science", "English"]

st.markdown(
    """
    <style>
      .stApp { background: #f5f7fb; }
      .block-container { padding-top: 2rem; padding-bottom: 2rem; }
      .hero {
        padding: 1.5rem 1.7rem; border-radius: 18px;
        background: linear-gradient(120deg, #153e75, #2878b5);
        color: white; margin-bottom: 1rem;
      }
      .hero h1 { color: white; margin: 0; font-size: 2rem; }
      .hero p { color: #e8f2ff; margin: .4rem 0 0 0; }
      div[data-testid="stMetric"] {
        background: white; border: 1px solid #e4eaf3;
        padding: 1rem; border-radius: 14px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🎓 Student Performance Analysis</h1>
      <p>Understand student results with clear statistics, editable records, and visual reports.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Session state keeps edits/additions while the app is running.
if "students_df" not in st.session_state:
    st.session_state.students_df = pd.DataFrame(SAMPLE_DATA)

with st.sidebar:
    st.header("⚙️ Settings")
    pass_mark = st.slider("Pass mark per subject", min_value=0, max_value=100, value=PASS_MARK)
    st.caption("A student passes when every subject mark is at least the selected pass mark.")
    if st.button("↩️ Reset sample data", use_container_width=True):
        st.session_state.students_df = pd.DataFrame(SAMPLE_DATA)
        st.rerun()

    st.divider()
    st.subheader("➕ Add a student")
    with st.form("add_student_form", clear_on_submit=True):
        new_name = st.text_input("Student name")
        new_math = st.number_input("Maths mark", min_value=0, max_value=100, value=70)
        new_science = st.number_input("Science mark", min_value=0, max_value=100, value=70)
        new_english = st.number_input("English mark", min_value=0, max_value=100, value=70)
        new_attendance = st.number_input("Attendance (%)", min_value=0, max_value=100, value=90)
        submitted = st.form_submit_button("Add student", use_container_width=True)
        if submitted:
            if not new_name.strip():
                st.error("Please enter a student name.")
            elif st.session_state.students_df["Student Name"].str.casefold().eq(new_name.strip().casefold()).any():
                st.error("A student with that name already exists.")
            else:
                new_row = pd.DataFrame([{
                    "Student Name": new_name.strip(),
                    "Maths": int(new_math),
                    "Science": int(new_science),
                    "English": int(new_english),
                    "Attendance (%)": int(new_attendance),
                }])
                st.session_state.students_df = pd.concat(
                    [st.session_state.students_df, new_row], ignore_index=True
                )
                st.success(f"Added {new_name.strip()}.")
                st.rerun()

df = st.session_state.students_df.copy()

if df.empty:
    st.info("No student records yet. Add a student from the sidebar to get started.")
    st.stop()

# Derived values are recalculated from the current records.
df["Total Marks"] = df[SUBJECTS].sum(axis=1)
df["Average (%)"] = df[SUBJECTS].mean(axis=1).round(2)
df["Result"] = df[SUBJECTS].ge(pass_mark).all(axis=1).map({True: "Pass", False: "Fail"})
df["Performance"] = df["Average (%)"].map(
    lambda average: "Excellent" if average >= 85 else
    "Good" if average >= 70 else
    "Needs Improvement" if average >= pass_mark else "At Risk"
)

# Filters
st.subheader("📋 Student records")
filter_col1, filter_col2 = st.columns([2, 1])
with filter_col1:
    search_name = st.text_input("Search by student name", placeholder="Type a name...")
with filter_col2:
    result_filter = st.selectbox("Filter by result", ["All", "Pass", "Fail"])

filtered = df.copy()
if search_name.strip():
    filtered = filtered[filtered["Student Name"].str.contains(search_name.strip(), case=False, na=False)]
if result_filter != "All":
    filtered = filtered[filtered["Result"] == result_filter]

st.caption("Edit the table directly. Changes update the statistics and charts for this session.")
edited = st.data_editor(
    filtered,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    disabled=["Total Marks", "Average (%)", "Result", "Performance"],
    column_config={
        "Maths": st.column_config.NumberColumn("Maths", min_value=0, max_value=100, step=1),
        "Science": st.column_config.NumberColumn("Science", min_value=0, max_value=100, step=1),
        "English": st.column_config.NumberColumn("English", min_value=0, max_value=100, step=1),
        "Attendance (%)": st.column_config.NumberColumn("Attendance (%)", min_value=0, max_value=100, step=1),
        "Average (%)": st.column_config.NumberColumn("Average (%)", format="%.2f%%"),
    },
    key="student_editor",
)

# Apply edited values back to the full dataset by student name.
# The name column is treated as an identifier in this small demo.
if not edited.empty:
    updated = st.session_state.students_df.copy()
    for _, row in edited.iterrows():
        match = updated["Student Name"] == row["Student Name"]
        if match.any():
            for col in ["Maths", "Science", "English", "Attendance (%)"]:
                updated.loc[match, col] = int(max(0, min(100, row[col])))
    st.session_state.students_df = updated

# Recompute after edits for accurate metrics and plots.
df = st.session_state.students_df.copy()
df["Total Marks"] = df[SUBJECTS].sum(axis=1)