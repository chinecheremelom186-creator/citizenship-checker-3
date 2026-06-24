import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="BIO 102 Pro Exam", layout="wide")

# --- INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'submitted' not in st.session_state: st.session_state.submitted = False

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
        else:
            st.error("Name is required!")
    st.stop()

# --- LOAD DATA ---
try:
    df = pd.read_csv('questions.csv')
except:
    st.error("questions.csv file not found!")
    st.stop()

# --- TIMER ---
remaining = 300 - (time.time() - st.session_state.start_time)
if remaining <= 0: 
    st.session_state.submitted = True

# --- EXAM FLOW ---
if not st.session_state.submitted:
    st.metric("Time Remaining", f"{int(remaining//60)}:{int(remaining%60):02d}")
    st.progress((st.session_state.q_index + 1) / len(df))
    
    row = df.iloc[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}: {row['question']}")
    
    ans = st.radio("Select:", [row['optionA'], row['optionB'], row['optionC']], key="current_q", index=None)
    
    if st.button("Next/Submit"):
        st.session_state.answers[st.session_state.q_index] = ans
        if st.session_state.q_index < len(df) - 1:
            st.session_state.q_index += 1
            st.rerun()
        else:
            st.session_state.submitted = True
            st.rerun()

# --- RESULTS & RANKING ---
if st.session_state.submitted:
    # 1. Calculate Score
    score = sum(1 for i, row in df.iterrows() if st.session_state.answers.get(i) == row['correct'])
    percent = (score / len(df)) * 100
    
    # 2. Save result
    result_data = pd.DataFrame([[st.session_state.name, score, percent]], columns=['name', 'score', 'percent'])
    result_data.to_csv('results.csv', mode='a', header=False, index=False)
    
    # 3. Display Ranking
    all_results = pd.read_csv('results.csv', names=['name', 'score', 'percent'])
    all_results = all_results.sort_values(by='score', ascending=False).reset_index(drop=True)
    my_rank = all_results[all_results['name'] == st.session_state.name].index[0] + 1
    
    st.success(f"Exam Finished! Score: {score}/{len(df)} ({percent:.1f}%)")
    st.subheader(f"🏆 Your Position: {my_rank} out of {len(all_results)}")
    
    for i, row in df.iterrows():
        with st.expander(f"Q{i+1} Review"):
            st.write(f"Explanation: {row['explanation']}")
