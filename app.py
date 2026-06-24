import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="BIO 102 Exam", layout="wide")

# Initialize State
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'submitted' not in st.session_state: st.session_state.submitted = False

st.title("🎓 BIO 102 Pro Exam")

# Admin Panel to add questions
with st.sidebar.expander("Admin: Add Question"):
    new_q = st.text_input("Question")
    a = st.text_input("Option A"); b = st.text_input("Option B"); c = st.text_input("Option C")
    corr = st.selectbox("Correct", ["Option A", "Option B", "Option C"])
    expl = st.text_area("Explanation")
    if st.button("Save to CSV"):
        pd.DataFrame([[new_q, a, b, c, corr, expl]], columns=['question','optionA','optionB','optionC','correct','explanation']).to_csv('questions.csv', mode='a', header=False, index=False)
        st.success("Added!")

# Load Questions
try:
    df = pd.read_csv('questions.csv')
except:
    st.error("questions.csv not found! Create it in GitHub.")
    st.stop()

# Timer Logic
remaining = 300 - (time.time() - st.session_state.start_time)
if remaining > 0 and not st.session_state.submitted:
    st.metric("Time Remaining", f"{int(remaining//60)}:{int(remaining%60):02d}")
    
    # Render Quiz
    user_answers = {}
    for i, row in df.iterrows():
        st.write(f"**Q{i+1}: {row['question']}**")
        user_answers[i] = st.radio(f"Select:", [row['optionA'], row['optionB'], row['optionC']], key=i, index=None)
    
    if st.button("Submit Exam"):
        st.session_state.submitted = True
        st.rerun()
else:
    st.session_state.submitted = True

# Results Logic
if st.session_state.submitted:
    score = 0
    skipped = 0
    for i, row in df.iterrows():
        ans = user_answers.get(i)
        if ans is None: skipped += 1
        elif ans == row['correct']: score += 1
    
    st.subheader("📊 Exam Results")
    st.write(f"Score: {score}/{len(df)} | Skipped: {skipped}")
    for i, row in df.iterrows():
        with st.expander(f"Review Q{i+1}"):
            st.write(f"Explanation: {row['explanation']}")
