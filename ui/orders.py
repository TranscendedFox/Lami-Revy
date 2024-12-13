import streamlit as st
from api.api import get_orders, remove_item_from_order, confirm_order
import json


def set_orders_page():
    st.title("Orders")

    if 'jwt_token' not in st.session_state or not st.session_state['jwt_token']:
        st.error("You must be logged in to view orders.")
        return

    orders_data = get_orders(st.session_state['jwt_token'])
    if orders_data:
        temp_order = orders_data.get("temp_order")
        if temp_order:
            total_price = 0
            st.subheader("Temporary Order")
            for item in temp_order.get("items"):
                total_price += item['price'] * item['quantity']
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    st.text(item["name"])
                with col2:
                    st.text(f"${item['price']:.2f}")
                with col3:
                    st.text(f"Quantity: {item['quantity']}")
                with col4:
                    if st.button("Remove", key=f"remove_item_{item['item_id']}"):
                        remove_item_from_order(st.session_state['jwt_token'], temp_order.get("order_id"),
                                               item['item_id'])
                        st.rerun()
            st.markdown("<h3 style='font-size: 16px;'>Order Summary</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns([2, 1])
            with col1:
                st.text(f"Order address: {temp_order.get('shipping_address')}")
            with col2:
                st.text(f"Total price: {total_price:.2f}")

            if st.button("Confirm Order", key="confirm_order"):
                confirm_order(st.session_state['jwt_token'])
                st.rerun()
        else:
            st.info("No temporary order available.")

        orders_history = orders_data.get("orders_history")
        if not orders_history:
            st.info("No order history available.")
        else:
            st.subheader("Order History")
            for i, order in enumerate(orders_history, start=1):
                total_price = 0
                with st.expander(f"Order {i}"):
                    st.markdown("<h3 style='font-size: 16px;'>Order Items</h3>", unsafe_allow_html=True)
                    for item in order.get("items", []):
                        total_price += item['price'] * item['quantity']
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.text(item["name"])
                        with col2:
                            st.text(f"${item['price']:.2f}")
                        with col3:
                            st.text(f"Quantity: {item['quantity']}")
                    st.markdown("<h3 style='font-size: 16px;'>Order Summary</h3>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.text(f"Order address: {order.get('shipping_address')}")
                    with col2:
                        st.text(f"Ordered at: {order.get('created_at')}")
                    with col3:
                        st.text(f"Total price: {total_price:.2f}")