import streamlit as st
from api.api import get_favorites, remove_favorite, add_item_to_order
import pandas as pd


def set_favorites_page():
    if 'jwt_token' not in st.session_state or not st.session_state['jwt_token']:
        st.error("You must be logged in to view favorite items.")
        return

    items_response = get_favorites(st.session_state['jwt_token'])

    if items_response:
        if items_response is not None:
            df = pd.DataFrame(items_response)

            st.header("Favorite Items")
            for index, row in df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
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
                        if st.button("Remove", key=f"remove_favorite_{row['item_id']}"):
                            remove_favorite(st.session_state['jwt_token'], row['item_id'])
                            st.rerun()

        else:
            st.error("Unexpected data format received.")
    else:
        st.error("No favorite items")
