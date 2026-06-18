import streamlit as st
import pandas as pd
import os

# Function to save data to a CSV file
def save_data(data):
    df = pd.DataFrame([data])
    # If the file doesn't exist, create it with headers
    if not os.path.exists('responses.csv'):
        df.to_csv('responses.csv', index=False)
    else:
        # Otherwise, append the data without adding headers again
        df.to_csv('responses.csv', mode='a', header=False, index=False)

st.title("🛂 CITIZENSHIP CHECKER")

age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

if st.button("Check Eligibility"):
    if age >= 18:
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
    else:
        st.warning("You must be 18+ to register.")

# Add a section to download the saved data
st.divider()
if os.path.exists('responses.csv'):
    with open("responses.csv", "rb") as file:
        st.download_button(
            label="Download All Responses (CSV)",
            data=file,
            file_name="responses.csv",
            mime="text/csv"
        )
