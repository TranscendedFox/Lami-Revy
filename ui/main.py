import streamlit as st
from api.api import get_jwt_token, get_all_items, search_items, add_favorites, add_item_to_order, reset_chat
import pandas as pd
from register import set_register_page
from favorites import set_favorites_page
from orders import set_orders_page
from chat import set_chat_page

if 'main' not in st.session_state:
    st.session_state['main'] = 'main'
if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None
if 'responses_count' not in st.session_state:
    st.session_state['responses_count'] = 0

st.title("Lamy Revi")

if st.session_state['jwt_token']:
    st.sidebar.header("Welcome!")
    if st.sidebar.button("Logout", key="sidebar_logout_button"):
        st.session_state['jwt_token'] = None
        st.session_state.show_registration_form = False  # Hide registration form
        st.sidebar.success("Logged out successfully!")
        st.rerun()
    if st.sidebar.button("Main page"):
        st.session_state['main'] = 'main'
    if st.sidebar.button("Favorites"):
        st.session_state['main'] = 'favorites'
    if st.sidebar.button("Orders"):
        st.session_state['main'] = 'orders'
    if st.sidebar.button("Chat"):
        reset_chat(st.session_state['jwt_token'])
        st.session_state['responses_count'] = 0
        st.session_state['main'] = 'chat'
else:
    st.sidebar.subheader("Login")
    login_username = st.sidebar.text_input("Username", key="login_username")
    login_password = st.sidebar.text_input("Password", type='password', key="login_password")
    if st.sidebar.button("Login", key="sidebar_login_button"):
        token = get_jwt_token(login_username, login_password)
        if token:
            st.session_state['jwt_token'] = token
            st.sidebar.success("Logged in successfully!")
            st.session_state.show_registration_form = False
            st.rerun()
        else:
            st.sidebar.error("Login failed. Check your credentials.")

    st.sidebar.subheader("New User?")
    if st.sidebar.button("Register", key="sidebar_register_button"):
        st.session_state['main'] = 'register'


if st.session_state['main'] == 'main':
    st.header("Search")
    search_query = st.text_input("Enter your search query:", key="search_bar")

    if st.button("Search", key="search_button"):
        items_data = search_items(search_query)
        if items_data:
            df = pd.DataFrame(items_data)

            st.header("Search Results")
            for index, row in df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])  # Adjust column widths as needed
                with col1:
                    st.text(row["name"])
                with col2:
                    st.text(f"${row['price']:.2f}")
                with col3:
                    st.text(f"Stock: {row['stock']}")
                with col4:
                    if st.session_state['jwt_token'] is not None:
                        if st.button("Add to Order", key=f"add_item_{row['item_id']}"):
                            add_item_to_order(st.session_state['jwt_token'], row['item_id'])
                with col5:
                    if st.session_state['jwt_token'] is not None:
                        if st.button("Add to Favorites", key=f"add_favorite_{row['item_id']}"):
                            add_favorites(st.session_state['jwt_token'], row['item_id'])
        else:
            st.error(f"No Results for {search_query}")
    else:
        items_response = get_all_items()

        if items_response:
            if items_response is not None:
                df = pd.DataFrame(items_response)
                st.header("Items")

                for index, row in df.iterrows():
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])  # Adjust column widths as needed
                    with col1:
                        st.text(row["name"])
                    with col2:
                        st.text(f"${row['price']:.2f}")
                    with col3:
                        st.text(f"Stock: {row['stock']}")
                    with col4:
                        if st.session_state['jwt_token'] is not None:
                            if st.button("Add to Order", key=f"add_item_{row['item_id']}"):
                                response = add_item_to_order(st.session_state['jwt_token'], row['item_id'])
                                if response['status'] == 'failed':
                                    st.error(response['message'])
                                else:
                                    st.success(response['message'])
                    with col5:
                        if st.session_state['jwt_token'] is not None:
                            if st.button("Add to Favorites", key=f"add_favorite_{row['item_id']}"):
                                response = add_favorites(st.session_state['jwt_token'], row['item_id'])
                                if response['status'] == 'failed':
                                    st.error(response['message'])
                                else:
                                    st.success(response['message'])
            else:
                st.error("Unexpected data format received.")
        else:
            st.error(f"Failed to fetch items. Status code: {items_response.status_code}")


if st.session_state['main'] == 'register' and not st.session_state['jwt_token']:
    set_register_page()

if st.session_state['main'] == 'favorites':
    set_favorites_page()

if st.session_state['main'] == 'orders':
    set_orders_page()

if st.session_state['main'] == 'chat':
    set_chat_page()
