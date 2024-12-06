import streamlit as st
from api.api import register_user, get_jwt_token, get_all_items, search_items
import pandas as pd

# Initialize session state variables
if 'main' not in st.session_state:
    st.session_state['main'] = True
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

# Register Content
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


# Main
if st.session_state['main']:
    st.header("Search")
    search_query = st.text_input("Enter your search query:", key="search_bar")

    # Simulate search functionality
    if st.button("Search", key="search_button"):
        items_data = search_items(search_query)
        if items_data:
            df = pd.DataFrame(items_data)

            st.header("Search Results")
            st.dataframe(df)
        else:
            st.error(f"No Results for {search_query}")

    items_response = get_all_items()

    if items_response:
        #items_data = items_response.json()
        if items_response is not None:
            df = pd.DataFrame(items_response)

            st.header("Items")
            st.dataframe(df)
        else:
            st.error("Unexpected data format received.")
    else:
        st.error(f"Failed to fetch items. Status code: {items_response.status_code}")