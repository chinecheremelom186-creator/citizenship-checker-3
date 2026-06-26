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
if 'start_time' not in st.session_state: st.session_state.start_time = None

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

# --- LIVE TIMER LOGIC ---
timer_placeholder = st.empty()
elapsed = time.time() - st.session_state.start_time
remaining = 300 - elapsed # 300 seconds = 5 minutes

if remaining <= 0:
    st.session_state.submitted = True
    st.rerun()
else:
    mins, secs = divmod(int(remaining), 60)
    timer_placeholder.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
    time.sleep(1) # This forces the timer to wait 1 second
    st.rerun() # This refreshes the page so the timer ticks

# --- EXAM FLOW ---
if not st.session_state.submitted:
    row = df.iloc[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}: {row['question']}")
    ans = st.radio("Select your answer:", [row['optionA'], row['optionB'], row['optionC']], key=f"q_{st.session_state.q_index}")
    
    col1, col2 = st.columns(2)
    if col1.button("Next Question"):
        st.session_state.answers[st.session_state.q_index] = ans
        if st.session_state.q_index < len(df) - 1:
            st.session_state.q_index += 1
            st.rerun()
    
    if col2.button("Submit Exam"):
        st.session_state.answers[st.session_state.q_index] = ans
        st.session_state.confirm_submit = True
    
    if st.session_state.confirm_submit:
        st.warning("⚠️ Are you sure? You cannot retake after submitting.")
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
    st.success(f"Exam Finished! Your Score: {score}/{len(df)} ({percent:.1f}%)")
    for i, row in df.iterrows():
        with st.expander(f"Q{i+1} Review"):
            st.write(f"Explanation: {row['explanation']}")
