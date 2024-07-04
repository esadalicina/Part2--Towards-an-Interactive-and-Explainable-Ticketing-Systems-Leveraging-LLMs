from streamlit_autorefresh import st_autorefresh
import base64
import streamlit as st
import pandas as pd
from streamlit_feedback import streamlit_feedback
import sys
import os

# Add the directory containing the Resources module to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Resources.data_access
from Resources.data_access import load_tickets, update_ticket
from Resources.chat_utils import init_db, add_message, get_messages


def ensure_arrow_compatibility(df):
    for column in df.columns:
        if df[column].dtype == 'object':
            try:
                # Try to convert the column to numeric type
                df[column] = pd.to_numeric(df[column])
            except ValueError:
                # If conversion fails, leave the column as it is
                pass
    return df


def send_message(sender, receiver, ticket_id, message=None, image_file=None):
    if message or image_file:
        image_data = image_file.read() if image_file else None
        add_message(sender, receiver, message, ticket_id, image=image_data)
        st.session_state['support_message'] = "  "


def display_messages(current_user, chat_with, ticket_id):

    messages = get_messages(current_user, chat_with, ticket_id)

    # CSS for styling
    st.markdown("""
        <style>
        .chat-history {
            max-height: 500px;
            height: 500px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #FFF;
        }
        .message {
            display: flex;
            align-items: center;
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
            justify-content: flex-end;
        }
        .message-user .message-content {
            background-color: #DCF8C6;
            text-align: right;
            border: 1px solid #d4d4d4;
        }
        .message-other {
            justify-content: flex-start;
        }
        .message-other .message-content {
            background-color: #FFF;
            text-align: left;
            border: 1px solid #d4d4d4;
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
                img_html = f'<div class="message message-user"><label class="message-content"><img src="data:image/png;base64,{image_data}" class="img-thumbnail"/></label><div class="icon">💬</div></div>'
                chat_container += img_html
            else:
                chat_container += f'<div class="message message-user"><div class="message-content">{msg}</div><div class="icon">💬</div></div>'
        else:
            if img:
                image_data = base64.b64encode(img).decode()
                img_html = f'<div class="message message-other"><label class="message-content"><img src="data:image/png;base64,{image_data}" class="img-thumbnail"/></label><div class="icon">👤</div></div>'
                chat_container += img_html
            else:
                chat_container += f'<div class="message message-other"><div class="message-content">{msg}</div><div class="icon">👤</div></div>'
    chat_container += '</div>'
    st.markdown(chat_container, unsafe_allow_html=True)


def chat_conversation(ticket_id, tickets):

    # Initialize the database for chat
    init_db()

    ticket = tickets.loc[tickets['id'] == ticket_id].squeeze()
    current_user = str(ticket_id)
    chat_with = ticket['Assigned_to']

    # Initialize session state for support_message if it doesn't exist
    if 'support_message' not in st.session_state:
        st.session_state['support_message'] = None

    with st.form(key='message_form'):

        # Display chat messages initially
        display_messages(current_user, chat_with, ticket_id)
        input_placeholder = st.empty()
        support_message = input_placeholder.text_area("You:", value=st.session_state['support_message'], height=100)
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Send")
        st.session_state['support_message'] = "   "

        if submitted:
            if support_message:
                send_message(current_user, chat_with, ticket_id, message=support_message)
                st.session_state['support_message'] = "  "

            if uploaded_file is not None:
                send_message(current_user, chat_with, ticket_id, image_file=uploaded_file)
                st.session_state['support_message'] = "   "

    # Auto-refresh every 1 seconds
    st_autorefresh(interval=1000, key="chat_refresh")


def ticket_information():

    st_autorefresh(interval=10000, key="refresh")

    tickets = ensure_arrow_compatibility(load_tickets())
    st.session_state.tickets = tickets

    # Load tickets from CSV
    if 'tickets' not in st.session_state:
        st.session_state.tickets = tickets

    # Define sidebar for ticket overview
    st.sidebar.subheader("Ticket Overview")

    # Display submitted and unsolved tickets in the sidebar

    st.sidebar.write("Solved Tickets")
    closed_tickets = st.session_state.tickets[st.session_state.tickets['Status'] == 'Closed']
    st.sidebar.write(closed_tickets[['id', 'Ticket Title', "Description", "Category", "Subcategory", "Assigned_to", "Submission Time", "Feedback Smiley", "Feedback Text"]])

    st.sidebar.write("Submitted Tickets")
    submitted_tickets = st.session_state.tickets[st.session_state.tickets['Status'] == 'Submitted']
    st.sidebar.write(submitted_tickets[['id', 'Ticket Title', "Description", "Category", "Subcategory", "Submission Time"]])

    ticket_title = ""
    if 'tickets' in st.session_state:
        st.sidebar.write("Tickets in Progress")
        progressed_tickets = st.session_state.tickets[(st.session_state.tickets['Status'] == 'In Progress') | (st.session_state.tickets['Status'] == 'User Feedback')]
        for index, ticket in progressed_tickets.iterrows():
            ticket_id = ticket['id']
            ticket_title = ticket['Ticket Title']
            if st.sidebar.button(f"View Ticket #{ticket_id}: {ticket_title}", key=f"view_ticket_{ticket_id}"):
                st.session_state.selected_ticket = ticket_id
                st.rerun()

    if 'selected_ticket' in st.session_state:
        ticket_id = st.session_state.selected_ticket
        specific = st.session_state.tickets[(st.session_state.tickets['id'] == ticket_id) & (st.session_state.tickets['Status'] == "In Progress")]
        if not specific.empty:
            ticket = st.session_state.tickets.loc[st.session_state.tickets['id'] == ticket_id].squeeze()
            st.header(f"Ticket #{ticket_id}")
            st.subheader(ticket_title)
            st.write(f"**Description:** {ticket['Description']}")
            st.write(f"**Category:** {ticket['Category']}")
            st.write(f"**Subcategory:** {ticket['Subcategory']}")
            st.write(f"**Assigned to:** {ticket['Assigned_to']}")
            st.write(f"**Submission Time:** {ticket['Submission Time']}")


            # Display chat conversation for the selected ticket
            chat_conversation(ticket_id, tickets)

        specific_ticket = st.session_state.tickets[(st.session_state.tickets['id'] == ticket_id) & (st.session_state.tickets['Status'] == "User Feedback")]
        if not specific_ticket.empty:
            with st.form(key=f"feed_{ticket_id}"):
                st.write(f"Feedback Ticket {ticket_id}")
                feed = streamlit_feedback(
                    feedback_type="faces",
                    align="flex-start",
                    key=f"feedback_{ticket_id}",
                )

                text = st.text_area("Please provide a description", key=f"text_{ticket_id}")

                feedback = st.form_submit_button("Submit Feedback")

                if feedback:
                    update_ticket(ticket_id, 'Feedback Smiley', feed['score'])
                    update_ticket(ticket_id, 'Feedback Text', text)
                    update_ticket(ticket_id, 'Status', "Closed")
                    st.rerun()

    else:
        st.write("No ticket selected or in progress.")
