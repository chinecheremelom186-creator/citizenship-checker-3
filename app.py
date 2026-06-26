import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="BIO 102 Pro Exam", layout="wide")

# --- INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'ready_to_start' not in st.session_state: st.session_state.ready_to_start = False
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'confirm_submit' not in st.session_state: st.session_state.confirm_submit = False
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

# --- LOAD QUESTIONS ---
df = pd.read_csv('questions.csv')

# --- LOGIN / ADMIN GATE ---
if not st.session_state.logged_in:
    st.title("BIO 102 Pro Exam")
    name = st.text_input("Enter your Full Name to Start:")
    # Admin access: type 'admin123' in the name field to open the tool
    if name == "admin123":
        st.session_state.admin_mode = True
        st.session_state.logged_in = True
    elif st.button("Continue"):
        if name:
            st.session_state.name = name
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Name is required!")
    if not st.session_state.admin_mode:
        st.stop()

# --- ADMIN TOOL ---
if st.session_state.admin_mode:
    st.header("🛠️ Admin: Add New Question")
    new_q = st.text_input("Question")
    optA = st.text_input("Option A")
    optB = st.text_input("Option B")
    optC = st.text_input("Option C")
    corr = st.text_input("Correct Answer (Exactly as written above)")
    expl = st.text_area("Explanation")
    if st.button("Save New Question"):
        st.write("Copy this line to your CSV file:")
        st.code(f'"{new_q}","{optA}","{optB}","{optC}","{corr}","{expl}"')
    st.stop()

# --- READY GATE ---
if not st.session_state.ready_to_start:
    st.subheader(f"Hello, {st.session_state.name}!")
    st.write("5-minute timer starts once you click 'Start Exam'.")
    col1, col2 = st.columns(2)
    if col1.button("Start Exam"):
        st.session_state.ready_to_start = True
        st.session_state.start_time = time.time()
        st.rerun()
    if col2.button("Quit"):
        st.warning("Exam cancelled.")
        st.stop()
    st.stop()

# --- TIMER & EXAM FLOW ---
if not st.session_state.submitted:
    elapsed = time.time() - st.session_state.start_time
    remaining = 300 - elapsed 
    if remaining <= 0:
        st.session_state.submitted = True
        st.rerun()
    
    mins, secs = divmod(int(remaining), 60)
    st.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
    
    row = df.iloc[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}: {row['question']}")
    ans = st.radio("Select:", [row['optionA'], row['optionB'], row['optionC']], key=f"q_{st.session_state.q_index}")
    
    c1, c2 = st.columns(2)
    if c1.button("Next Question"):
        st.session_state.answers[st.session_state.q_index] = ans
        if st.session_state.q_index < len(df) - 1:
            st.session_state.q_index += 1
            st.rerun()
    if c2.button("Submit Exam"):
        st.session_state.answers[st.session_state.q_index] = ans
        st.session_state.confirm_submit = True
    
    if st.session_state.confirm_submit:
        if st.button("YES, SUBMIT"):
            st.session_state.submitted = True
            st.rerun()
            
    time.sleep(1)
    st.rerun()

# --- RESULTS ---
if st.session_state.submitted:
    score = sum(1 for i, row in df.iterrows() if st.session_state.answers.get(i) == row['correct'])
    st.success(f"Score: {score}/{len(df)}")
