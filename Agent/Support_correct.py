import base64
import ssl
import certifi
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_autorefresh import st_autorefresh
from Admin_correct import *
from User_Feedback import *
import sys
import os

# Add the directory containing the Resources module to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Resources.data_access
from Resources.data_access import load_tickets, update_ticket, get_email_address
from Resources.chat_utils import init_db, add_message, get_messages


def login(username, password):
    user_data = users[(users['name'] == username) & (users['password'] == password)]
    if not user_data.empty:
        st.session_state.logged_in = True
        st.session_state.user = username
        st.session_state.team = user_data['team'].values[0]
        st.session_state.role = user_data['role'].values[0]
        st.session_state.category = user_data['category'].values[0]
        succ = st.success('Login successful!', icon="✅")
        time.sleep(3)
        succ.empty()
    else:
        ss = st.error('Invalid username or password', icon="🚨")
        time.sleep(3)
        ss.empty()


def send_notification(email):
    sender_email = "cfpb.helpdesk@gmail.com"  # Replace with your Gmail address
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ticket Notification ✅"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Your ticket has been assigned to a support agent. Please log in to your account to have a chat 😀"
    part1 = MIMEText(text, "plain")

    # Attach parts into message container
    message.attach(part1)

    try:
        context = ssl.create_default_context(cafile=certifi.where())
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, 'pbfc gvpl atax gfge')  # Use the app password here
            server.sendmail(sender_email, receiver_email, message.as_string())

    except Exception as e:
        st.error(f"Error sending notification email: {e}", icon="🚨")


def update_ticket_status(ticket_id, status, user=None):
    update_ticket(ticket_id, "Status", status)
    update_ticket(ticket_id, "Assigned_to", user)
    st.rerun()


def send_message(sender, receiver, ticket_id, message=None, image_file=None):
    if message or image_file:
        image_data = image_file.read() if image_file else None
        add_message(sender, receiver, message, ticket_id, image=image_data)
        st.session_state['support_message'] = "  "


def display_messages(current_user, chat_with, ticket_id):
    messages = get_messages(current_user, chat_with, ticket_id)

    st.markdown("""
    <style>
    .chat-history {
        max-height: 400px;
        height: 400px;
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


def ticket_chat_page(ticket_id):
    init_db()

    current_user = st.session_state.user
    chat_with = str(ticket_id)

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

    # Auto-refresh every 2 seconds
    st_autorefresh(interval=1000, key="chat_refresh")


def reclassify_ticket(ticket_id, new_category, new_subcategory):
    update_ticket(ticket_id, 'Category', new_category)
    update_ticket(ticket_id, 'Subcatgeory', new_subcategory)
    update_ticket(ticket_id, 'Status', 'Submited')


def mark_ticket_wrong_classification(ticket_id):
    update_ticket(ticket_id, 'Status', 'Wrong Classification')


def display_ticket_info(ticket_id):
    ticket = tickets.loc[tickets['id'] == ticket_id].squeeze()

    st.markdown(f"### Ticket #{ticket['id']}")
    st.write(f"**Title:** {ticket['Ticket Title']}")
    st.write(f"**Description:** {ticket['Description']}")
    st.write(f"**Priority:** {ticket['Priority']}")
    st.write(f"**Status:** {ticket['Status']}")

    ticket_chat_page(ticket_id)

    if ticket['Status'] != 'User Feedback':
        if st.button("Close Ticket", key=f"close_{ticket['id']}"):
            update_ticket_status(ticket['id'], 'User Feedback', st.session_state.user)
            st.success(f'Ticket closed.')
            # st.session_state.selected_ticket = None
            st.rerun()


def my_tickets_page():
    st.header(f'My Tickets ({st.session_state.user})')

    # Filter tickets assigned to current user and not closed
    my_tickets = tickets[(tickets['Assigned_to'] == st.session_state.user) & (tickets['Status'] != 'User Feedback') & (tickets['Status'] != 'Closed')]

    if my_tickets.empty:
        st.write("No tickets assigned to you.")
    else:
        # Group tickets by priority
        priority_groups = my_tickets.groupby('Priority')

        # Priority selection
        priority_options = ['All'] + list(priority_groups.groups.keys())
        selected_priority = st.selectbox("Select Priority", priority_options)

        if selected_priority == 'All':
            filtered_tickets = my_tickets
        else:
            filtered_tickets = priority_groups.get_group(selected_priority)

        # Display tickets by selected priority
        if not filtered_tickets.empty:
            selected_ticket = st.selectbox("Select a ticket", filtered_tickets['id'])
            display_ticket_info(selected_ticket)


def update_subcategory():
    st.session_state.selected_subcategory = ""


def main(users, tickets):
    # Initialize session state variables if they don't exist

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'team' not in st.session_state:
        st.session_state.team = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'category' not in st.session_state:
        st.session_state.category = None
    if 'page' not in st.session_state:
        st.session_state.page = 'Dashboard'
    # if 'selected_ticket' not in st.session_state:
    #     st.session_state.selected_ticket = None
    if "new_member_name" not in st.session_state:
        st.session_state.new_member_name = ""
    if "new_member_password" not in st.session_state:
        st.session_state.new_member_password = ""
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_subcategory" not in st.session_state:
        st.session_state.selected_subcategory = None
    if "sele_category" not in st.session_state:
        st.session_state.sele_category = ""
    if "sele_subcategory" not in st.session_state:
        st.session_state.sele_subcategory = ""

    if not st.session_state.logged_in:
        st.title('Support Ticketing System')
        st.subheader('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            login(username, password)
            st.rerun()
    else:
        st.sidebar.title(f'Welcome, {st.session_state.user}')
        st.sidebar.write(f'Category: {st.session_state.category}')
        st.sidebar.write(f'Team: {st.session_state.team}')
        st.sidebar.write(f'Role: {st.session_state.role}')

        if st.sidebar.button('Logout'):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.team = None
            st.session_state.role = None
            st.session_state.category = None
            st.session_state.page = 'Dashboard'
            # st.session_state.selected_ticket = None
            st.rerun()

        if st.session_state.role == 'admin':
            pages = ["Dashboard", "Ticket Updates", "Ticket Information", "User Feedback", "Conversation"]
        else:
            pages = ["Tickets", "My Tickets", "User Feedback"]

        if st.session_state.page not in pages:
            st.session_state.page = pages[0]

        page = st.sidebar.radio("Navigation", pages, index=pages.index(st.session_state.page))
        st.session_state.page = page

        st.title(page)

        if page == "Dashboard" and st.session_state.role == 'admin':

            support_info(st, subcategories, update_subcategory, users)

            add_support(st, update_subcategory, subcategories, users)

            remove_support(st, update_subcategory, subcategories, users)

        elif page == "Ticket Updates" and st.session_state.role == 'admin':

            reclassify(st, subcategories, update_subcategory, tickets, reclassify_ticket, load_tickets)

        elif page == "Ticket Information" and st.session_state.role == 'admin':
            get_info(st, tickets)

        elif page == "User Feedback" and st.session_state.role == 'admin':
            feedback_page(users, tickets)

        # elif page == "Conversation" and st.session_state.role == 'admin':
        #     conversation(st, save_message, users)

        elif page == "Tickets" and st.session_state.role != 'admin':
            st_autorefresh(interval=5000, key="chatrefresh")
            st.header(f'Tickets and Team Chat for {st.session_state.team} Team')
            team_tickets = tickets[
                (tickets['Subcategory'] == st.session_state.team) & (tickets['Status'] != 'User Feedback') & (
                            tickets['Status'] != 'In Progress') & (tickets['Status'] != 'Wrong Classification') & (
                            tickets['Status'] != 'Closed')]

            priority_filter = st.selectbox('Filter by priority', ['All', 'Low', 'Medium', 'High'])
            if priority_filter != 'All':
                team_tickets = team_tickets[team_tickets['Priority'] == priority_filter]

            st.dataframe(team_tickets[['id', "Tags", "Ticket Title", "Ticket Summary"]], use_container_width=True)

            ticket_id = st.selectbox('Enter Ticket ID to Accept', team_tickets['id'])
            if st.button('Accept Ticket'):
                st.success(f'Ticket {ticket_id} accepted.', icon="✅")
                email = get_email_address(ticket_id)
                send_notification(email)
                update_ticket_status(ticket_id, 'In Progress', st.session_state.user)
                load_tickets()  # Reload tickets to get updated data

            st.subheader('Mark Ticket as Wrongly Classified')
            ticket_id_wrong_classification = st.selectbox('Enter Ticket ID to send to Admin',
                                                          [""] + list(team_tickets['id']))

            if st.button('Mark as Wrongly Classified'):
                st.success(f'Ticket {ticket_id_wrong_classification} marked as wrongly classified.', icon="✅")
                mark_ticket_wrong_classification(ticket_id_wrong_classification)
                load_tickets()  # Reload tickets to get updated data

            # st.subheader('Team Chat')
            # chat_message = st.text_area('Enter your message')
            # if st.button('Send Chat Message'):
            #     save_message(st.session_state.user, st.session_state.team, chat_message, team_chat=True)
            #     st.success('Message sent to team chat.')
            #
            # # new
            # st.subheader('Chat Messages')
            # team_chat_messages = load_messages(team=st.session_state.team)
            # for _, message in team_chat_messages.iterrows():
            #     st.write(f"**{message['sender']}**: {message['message']}")
            # new

        elif page == "My Tickets" and st.session_state.role != 'admin':
            my_tickets_page()

        elif page == "User Feedback" and st.session_state.role != 'admin':
            user_feedback_page(st.session_state.user)


if __name__ == "__main__":
    users = pd.read_csv('/Users/esada/Desktop/pythonProject/data/users.csv')
    tickets = load_tickets()
    main(users, tickets)
