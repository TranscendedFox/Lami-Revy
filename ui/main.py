import streamlit as st
from api.api import register_user, get_jwt_token

# Initialize session state variables
if 'show_registration_form' not in st.session_state:
    st.session_state['show_registration_form'] = False
if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None

st.title("Lamy Revi")

# Sidebar User Management
if st.session_state['jwt_token']:
    # Show Logout button when logged in
    st.sidebar.header("Welcome!")
    if st.sidebar.button("Logout", key="sidebar_logout_button"):
        st.session_state['jwt_token'] = None
        st.session_state.show_registration_form = False  # Hide registration form
        st.sidebar.success("Logged out successfully!")
        st.rerun()
else:
    # Show Login form when not logged in
    st.sidebar.subheader("Login")
    login_username = st.sidebar.text_input("Username", key="login_username")
    login_password = st.sidebar.text_input("Password", type='password', key="login_password")
    if st.sidebar.button("Login", key="sidebar_login_button"):
        token = get_jwt_token(login_username, login_password)
        if token:
            st.session_state['jwt_token'] = token
            st.sidebar.success("Logged in successfully!")
            st.session_state.show_registration_form = False  # Hide registration form
            st.rerun()
        else:
            st.sidebar.error("Login failed. Check your credentials.")

    # Show Register button when not logged in
    st.sidebar.subheader("New User?")
    if st.sidebar.button("Register", key="sidebar_register_button"):
        st.session_state.show_registration_form = True

# Main Content
if st.session_state.show_registration_form and not st.session_state['jwt_token']:
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
