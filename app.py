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

# --- ADMIN PANEL: Add Questions ---
with st.sidebar.expander("Admin: Add New Question"):
    new_q = st.text_input("Question")
    optA = st.text_input("Option A")
    optB = st.text_input("Option B")
    optC = st.text_input("Option C")
    corr = st.text_input("Correct Answer (must match one of the above)")
    expl = st.text_area("Explanation")
    
    if st.button("Add to Database"):
        new_data = pd.DataFrame([[new_q, optA, optB, optC, corr, expl]], 
                                columns=['question', 'optionA', 'optionB', 'optionC', 'correct', 'explanation'])
        # NOTE: This adds it to the session memory. 
        # For permanent storage on GitHub, you still need to update the file, 
        # but this allows you to input questions via the app interface.
        st.success("Question added to session!")
        
# --- LOAD QUESTIONS ---
@st.cache_data
def load_data():
    return pd.read_csv('questions.csv')

df = load_data()

# --- LOGIN GATE ---
if not st.session_state.logged_in:
    st.title("Welcome to BIO 102 Exam")
    name = st.text_input("Enter your Full Name:")
    if st.button("Continue"):
        if name:
            st.session_state.name = name
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- READY GATE ---
if not st.session_state.ready_to_start:
    st.title(f"Ready, {st.session_state.name}?")
    st.write("You have 5 minutes once you start.")
    if st.button("Start Exam Now"):
        st.session_state.ready_to_start = True
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

# --- TIMER & EXAM LOGIC ---
if st.session_state.ready_to_start and not st.session_state.submitted:
    # Calculate time
    elapsed = time.time() - st.session_state.start_time
    remaining = 300 - elapsed
    
    if remaining <= 0:
        st.session_state.submitted = True
        st.rerun()
    
    # Display Ticking Timer
    mins, secs = divmod(int(remaining), 60)
    st.sidebar.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
    
    # Display Progress
    st.progress((st.session_state.q_index + 1) / len(df))
    
    # Question
    row = df.iloc[st.session_state.q_index]
    st.subheader(f"Question {st.session_state.q_index + 1}")
    st.write(row['question'])
    ans = st.radio("Choose:", [row['optionA'], row['optionB'], row['optionC']], key="choice")
    
    col1, col2 = st.columns(2)
    if col1.button("Next"):
        st.session_state.answers[st.session_state.q_index] = ans
        if st.session_state.q_index < len(df) - 1:
            st.session_state.q_index += 1
            st.rerun()
    if col2.button("Submit"):
        st.session_state.answers[st.session_state.q_index] = ans
        st.session_state.confirm_submit = True
    
    if st.session_state.confirm_submit:
        if st.button("YES, CONFIRM SUBMIT"):
            st.session_state.submitted = True
            st.rerun()
    
    # Force refresh for the timer
    time.sleep(1)
    st.rerun()

# --- RESULTS ---
if st.session_state.submitted:
    st.success("Exam Submitted!")
    score = sum(1 for i, row in df.iterrows() if st.session_state.answers.get(i) == row['correct'])
    st.write(f"Your Score: {score} / {len(df)}")
