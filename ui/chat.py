import streamlit as st
from api.api import get_chat, set_message


def set_chat_page():
    st.title("Chat")

    chat_history = get_chat(st.session_state['jwt_token'])
    responses_count = 0
    if chat_history is not None:
        for chat in chat_history:
            if chat['role'] == 'user':
                st.markdown(f"**You:** {chat['content']}")
            elif chat['role'] == 'assistant':
                st.markdown(f"**Assistant:** {chat['content']}")
                responses_count += 1
            st.session_state['main'] = 'chat'
        st.session_state['responses_count'] = responses_count

    if st.session_state['responses_count'] < 5:
        user_input = st.text_input("Type your message:", key="user_input")
        if st.button("Send"):
            if user_input.strip():
                set_message(st.session_state['jwt_token'], user_input)
                st.rerun()
            else:
                st.error("Message cannot be empty.")
    else:
        st.error("Maximum messages sent.")
