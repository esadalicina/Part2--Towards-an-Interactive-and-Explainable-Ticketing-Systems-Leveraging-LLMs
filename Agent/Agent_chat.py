import base64
import streamlit as st
import sys
import os

# Add the directory containing the Resources module to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Resources.data_access
from Resources.chat_agent_utils import init_db, add_message, get_messages


def send_message(sender, receiver, group_id, message=None, image_file=None):
    """Send a message to a group."""
    if message or image_file:
        image_data = image_file.read() if image_file else None
        add_message(sender, receiver, group_id, message, image_data)


def display_messages(group_id, current_user, user):
    """Display messages for a specific group."""
    messages = get_messages(group_id)  # Fetch messages for the current user and group

    # CSS for styling
    st.markdown("""
            <style>
            .chat-history {
                max-height: 500px;
                height: 350px;
                overflow-y: auto;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #FFF;
            }
            .message {
                display: flex;
                flex-direction: column; /* Arrange user name above message */
                align-items: flex-start; /* Align messages to the left */
                margin-bottom: 10px;
            }
            .message-content {
                padding: 10px;
                border-radius: 10px;
                word-wrap: break-word;
                max-width: 80%;
                cursor: pointer; /* Add cursor pointer for clickable effect */
                position: relative; /* Required for absolutely positioned elements */
            }
            .message-content img {
                max-width: 100%; /* Ensure images fit within container */
                height: auto;
                display: block;
            }
            .message-user {
                align-items: flex-end; /* Align user's own messages to the right */
            }
            .message-user .message-content {
                background-color: #DCF8C6;
                text-align: right;
                border: 1px solid #d4d4d4;
            }
            .message-other {
                align-items: flex-start; /* Align other users' messages to the left */
            }
            .message-other .message-content {
                background-color: #FFF;
                text-align: left;
                border: 1px solid #d4d4d4;
            }
            .user-name {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .icon {
                margin: 0 10px;
            }
            .message-user .icon {
                order: 1;
            }
            .message-other .icon {
                order: -1;
            }
            /* CSS for enlarged image */
            .enlarged-image-checkbox {
                display: none; /* Hide the checkbox */
            }
            .enlarged-image-label {
                display: none; /* Initially hide the label */
                position: fixed;
                z-index: 2;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.9);
                text-align: center;
            }
            .enlarged-image-label img {
                max-width: 80%;
                max-height: 80%;
                margin-top: 10%; /* Adjust margin to center image vertically */
            }
            .message-content:hover .enlarged-image-label {
                display: block; /* Show label on hover */
            }
            </style>
            """, unsafe_allow_html=True)

    # HTML generation for chat history
    chat_container = '<div class="chat-history">'
    for sender, msg, img, timestamp in messages:
        if sender == current_user:
            if img:
                image_data = base64.b64encode(img).decode()
                img_html = f'<div class="message message-user"><div class="user-name">{current_user}</div><label class="message-content"><img src="data:image/png;base64,{image_data}" class="img-thumbnail"/></label></div>'
                chat_container += img_html
            else:
                chat_container += f'<div class="message message-user"><div class="user-name">{current_user}</div><div class="message-content">{msg}</div></div>'
        else:
            if img:
                image_data = base64.b64encode(img).decode()
                img_html = f'<div class="message message-other"><div class="user-name">{sender}</div><label class="message-content"><img src="data:image/png;base64,{image_data}" class="img-thumbnail"/></label></div>'
                chat_container += img_html
            else:
                chat_container += f'<div class="message message-other"><div class="user-name">{sender}</div><div class="message-content">{msg}</div></div>'
    chat_container += '</div>'
    st.markdown(chat_container, unsafe_allow_html=True)


def chat_conversation(team, username):
    """Streamlit UI for chat conversation."""

    # Initialize the database
    init_db()


    current_user = st.session_state.user  # Current logged-in user
    chat_with = team  # Change this to the agent or team you want to chat with

    # Initialize session state for support_message if it doesn't exist
    if 'support_message' not in st.session_state:
        st.session_state['support_message'] = None

    with st.form(key='message_form'):
        # Display chat messages initially
        display_messages(chat_with, current_user, username)

        input_placeholder = st.empty()
        support_message = input_placeholder.text_area("You:", value=st.session_state['support_message'], height=100)
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Send")
        st.session_state['support_message'] = "   "

        if submitted:
            if support_message:
                send_message(current_user, chat_with, team, message=support_message)
                st.session_state['support_message'] = "  "

            if uploaded_file is not None:
                send_message(current_user, chat_with, team, image_file=uploaded_file)
                st.session_state['support_message'] = "   "

