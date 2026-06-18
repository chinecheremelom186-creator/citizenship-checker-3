import streamlit as st
import pandas as pd
import os

# Function to save data
def save_data(data):
    df = pd.DataFrame([data])
    if not os.path.exists('responses.csv'):
        df.to_csv('responses.csv', index=False)
    else:
        df.to_csv('responses.csv', mode='a', header=False, index=False)

st.title("🛂 CITIZENSHIP CHECKER")

# The Form
with st.form("citizenship_form", clear_on_submit=True):
    name = st.text_input("Name:")
    school = st.text_input("School:")
    reg = st.text_input("Reg Number:")
    phone = st.text_input("Phone Number:")
    friend = st.text_input("Best friend's name:")
    submitted = st.form_submit_button("Submit Details")
    
    if submitted:
        new_data = {"Name": name, "School": school, "Reg": reg, "Phone": phone, "Friend": friend}
        save_data(new_data)
        st.success("Details saved successfully!")

# The Download Button
st.divider()
st.subheader("Admin Access")
if os.path.exists('responses.csv'):
    with open("responses.csv", "rb") as file:
        st.download_button(
            label="Download All Responses (CSV)",
            data=file,
            file_name="responses.csv",
            mime="text/csv"
        )
else:
    st.write("No responses yet. Please submit the form first.")
