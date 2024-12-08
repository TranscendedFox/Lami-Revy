import streamlit as st
from api.api import register_user

def set_register_page():
    st.header("Register")
    username = st.text_input("Username", key="register_username")
    first_name = st.text_input("First Name", key="register_firstname")
    last_name = st.text_input("Last Name", key="register_lastname")
    email = st.text_input("Email", key="register_email")
    phone = st.text_input("Phone", key="register_phone")
    address_country = st.text_input("Country", key="register_address_country")
    address_city = st.text_input("City", key="register_address_city")
    password = st.text_input("Password", type='password', key="register_password")

    if st.button("Register", key="form_register_button"):
        register_response = register_user(username, first_name, last_name, email, phone, address_city, address_country,
                                          password)
        if register_response.status_code == 201:
            st.success("Registered successfully!")
            st.session_state.show_registration_form = False  # Hide registration form after success
        else:
            st.error("Failed to register.")