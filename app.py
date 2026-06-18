import streamlit as st
import pandas as pd
import os

# --- SET YOUR PASSWORD HERE ---
ADMIN_PASSWORD = "gift031" 

def save_data(data):
    df = pd.DataFrame([data])
    if not os.path.exists('responses.csv'):
        df.to_csv('responses.csv', index=False)
    else:
        df.to_csv('responses.csv', mode='a', header=False, index=False)

st.set_page_config(page_title="Citizenship Checker", page_icon="🛂")

st.title("🛂 CITIZENSHIP CHECKER")
age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

if st.button("Check Eligibility"):
    if age >= 18:
        with st.form("citizenship_form", clear_on_submit=True):
            name = st.text_input("Name:")
            school = st.text_input("School:")
            nationality = st.text_input("Nationality:")
            state = st.text_input("State:")
            phone = st.text_input("Phone Number:")
            friend = st.text_input("Best friend's name:")
            submitted = st.form_submit_button("Submit Details")
            
            if submitted:
                new_data = {
                    "Name": name, 
                    "School": school, 
                    "Nationality": nationality, 
                    "State": state, 
                    "Phone": phone, 
                    "Friend": friend
                }
                save_data(new_data)
                st.success("Details saved successfully!")
    else:
        st.warning("You must be 18+ to register.")

st.divider()
st.subheader("Admin Access")
password = st.text_input("Enter Admin Password to Download Data:", type="password")

if password == ADMIN_PASSWORD:
    if os.path.exists('responses.csv'):
        with open("responses.csv", "rb") as file:
            st.download_button(label="Download All Responses (CSV)", data=file, file_name="responses.csv", mime="text/csv")
    else:
        st.write("No responses yet.")
elif password:
    st.error("Incorrect password.")
