import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="BIO 102 Exam", layout="wide")

# Persistent State
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}

st.title("🎓 BIO 102 Pro Exam")

# Admin Sidebar
with st.sidebar.expander("Admin: Add Question"):
    new_q = st.text_input("Question")
    a = st.text_input("Option A"); b = st.text_input("Option B"); c = st.text_input("Option C")
    corr = st.selectbox("Correct", [a, b, c])
    expl = st.text_area("Explanation")
    if st.button("Save"):
        pd.DataFrame([[new_q, a, b, c, corr, expl]], columns=['question','optionA','optionB','optionC','correct','explanation']).to_csv('questions.csv', mode='a', header=False, index=False)
        st.success("Added!")

# Load Data
try:
    df = pd.read_csv('questions.csv')
except:
    st.error("Missing questions.csv file.")
    st.stop()

# Timer and Quiz Logic
remaining = 300 - (time.time() - st.session_state.start_time)

if remaining > 0 and not st.session_state.submitted:
    st.metric("Time Remaining", f"{int(remaining//60)}:{int(remaining%60):02d}")
    
    for i, row in df.iterrows():
        st.write(f"**Q{i+1}: {row['question']}**")
        st.session_state.user_answers[i] = st.radio(f"Select:", [row['optionA'], row['optionB'], row['optionC']], key=f"q{i}", index=None)
    
    if st.button("Submit Exam"):
        st.session_state.submitted = True
        st.rerun()
else:
    if not st.session_state.submitted:
        st.session_state.submitted = True
        st.rerun()

# Results Logic
if st.session_state.submitted:
    score = 0
    skipped = 0
    st.subheader("📊 Exam Results")
    for i, row in df.iterrows():
        ans = st.session_state.user_answers.get(i)
        if ans is None: skipped += 1
        elif ans == row['correct']: score += 1
    
    st.write(f"Score: {score}/{len(df)} | Skipped: {skipped}")
    for i, row in df.iterrows():
        with st.expander(f"Review Q{i+1}"):
            st.write(f"Correct: {row['correct']} | Explanation: {row['explanation']}")
