import streamlit as st

# Set page configuration
st.set_page_config(page_title="Citizenship Checker", page_icon="🛂")

def main():
    st.title("🛂 CITIZENSHIP CHECKER")
    st.markdown("---")

    # Age input using a number input widget
    age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

    # Only show the form if the button is clicked
    if st.button("Check Eligibility"):
        if age >= 18:
            st.success("Hello dear, you can enter!")
            
            # Use a form to collect information
            with st.form("citizenship_form"):
                name = st.text_input("Name:")
                school = st.text_input("School:")
                reg = st.text_input("Reg Number:")
                phone = st.text_input("Phone Number:")
                friend = st.text_input("Best friend's name:")
                
                submitted = st.form_submit_button("Submit Details")
                
                if submitted:
                    st.divider()
                    st.write("### Registration Details")
                    st.info(f"**Name:** {name}\n\n**School:** {school}\n\n**Reg:** {reg}\n\n**Phone:** {phone}\n\n**Friend:** {friend}")
        else:
            st.warning("Na only here adulthood help.")
            st.write("BETTER ENJOY YOUR CHILDHOOD NOW, because hmmm...")
            st.error("Go and get your PVC, e get why, so that you can become an adult.")

if __name__ == "__main__":
    main()
