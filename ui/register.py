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
    gender = st.selectbox("Gender", options=["Male", "Female"], key="register_gender")
    age = st.number_input("Age", min_value=0, max_value=120, step=1, key="register_age")
    annual_income = st.number_input("Annual Income ($)", min_value=0.0, step=1000.0, key="register_annual_income")

    if st.button("Register", key="form_register_button"):
        user_request = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "address_city": address_city,
            "address_country": address_country,
            "password": password,
            "gender": gender,
            "age": age,
            "annual_income": annual_income
        }

        register_response = register_user(**user_request)

        if register_response.status_code == 201:
            st.success("Registered successfully!")
            st.session_state.show_registration_form = False
        else:
            st.error("Failed to register.")
