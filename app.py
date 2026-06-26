import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="BIO 102 Pro Exam", layout="wide")

# --- INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'confirm_submit' not in st.session_state: st.session_state.confirm_submit = False

# --- LOGIN GATE ---
if not st.session_state.logged_in:
    st.title("Welcome to BIO 102 Exam")
    name = st.text_input("Enter your Full Name to Start:")
    if st.button("Start Exam"):
        if name:
            st.session_state.name = name
            st.session_state.logged_in = True
            st.session_state.start_time = time.time()
            st.rerun()
    st.stop()

# --- LOAD DATA ---
df = pd.read_csv('questions.csv')

# --- EXAM FLOW ---
if not st.session_state.submitted:
    row = df.iloc[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}: {row['question']}")
    ans = st.radio("Select:", [row['optionA'], row['optionB'], row['optionC']], key=f"q_{st.session_state.q_index}")
    
    col1, col2 = st.columns(2)
    
    # NAVIGATION
    if col1.button("Next Question"):
        st.session_state.answers[st.session_state.q_index] = ans
        if st.session_state.q_index < len(df) - 1:
            st.session_state.q_index += 1
            st.rerun()
    
    # SUBMISSION LOGIC
    if col2.button("Submit Exam"):
        st.session_state.answers[st.session_state.q_index] = ans
        st.session_state.confirm_submit = True
    
    if st.session_state.confirm_submit:
        st.warning("⚠️ Are you sure you want to submit? You cannot retake the exam.")
        c1, c2 = st.columns(2)
        if c1.button("YES, SUBMIT"):
            st.session_state.submitted = True
            st.rerun()
        if c2.button("NO, GO BACK"):
            st.session_state.confirm_submit = False
            st.rerun()

# --- RESULTS ---
if st.session_state.submitted:
    score = sum(1 for i, row in df.iterrows() if st.session_state.answers.get(i) == row['correct'])
    percent = (score / len(df)) * 100
    st.success(f"Exam Finished! Score: {score}/{len(df)} ({percent:.1f}%)")
    for i, row in df.iterrows():
        with st.expander(f"Q{i+1} Review"):
            st.write(f"Explanation: {row['explanation']}")
