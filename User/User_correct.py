import streamlit.components.v1 as components
from User_TicketSubmission import *
from User_TickeInfos import *
from User_Registration import create_tables, get_email, check_user, email_confirmation_page, registration_page


def navigate_to_page(page_name):
    st.experimental_set_query_params(page=page_name)
    st.rerun()

def login_page():
    st.header("Welcome to the User Ticketing Website")
    st.subheader("Please login to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register", key='go_to_registration', use_container_width=True):
        st.session_state.page = 'Registration'
        st.rerun()

    if st.button("Login", use_container_width=True):
        if check_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = 'Home'
            succes = st.success("Logged in successfully!", icon="✅")
            time.sleep(1)  # Wait for 3 seconds
            succes.empty()
            st.rerun()
        else:
            error = st.error("Invalid username or password", icon="🚨")
            time.sleep(3)  # Wait for 3 seconds
            error.empty()


def main():
    df = pd.read_csv("/mount/src/ticketing-system/Data/KB_dataset.csv")

    # Initialize session state for login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = None

    if "email" not in st.session_state:
        st.session_state.email = None

    st.session_state.tickets = ensure_arrow_compatibility(load_tickets())

    st.session_state.email = get_email(st.session_state.username)

    # Registration page
    if 'page' not in st.session_state:
        st.session_state.page = 'Login'

    # Handle query parameters for email confirmation
    query_params = st.query_params.to_dict()
    if 'page' in query_params:
        st.session_state.page = query_params['page']
    if 'token' in query_params and st.session_state.page == 'Confirm_Email':
        token = query_params['token']
        email_confirmation_page(token)
        return

    # Login page
    if not st.session_state.logged_in:
        st.set_page_config(layout="centered")

        if st.session_state.page == 'Login':
            login_page()

        elif st.session_state.page == 'Registration':
            username, email = registration_page()
            st.session_state.username = username

        elif st.session_state.page == 'Confirm_Email':
            token = st.session_state.token if 'token' in st.session_state else ""
            email_confirmation_page(token)
    else:

        if 'page' not in st.session_state:
            st.session_state.page = 'Home'

        if st.session_state.page == 'Home':
            if st.button('Ticket Submission', key='submission', use_container_width=True):
                st.session_state.page = 'Ticket Submission'
                st.rerun()
            if st.button('Ticket Information', key='information', use_container_width=True):
                st.session_state.page = 'Ticket Information'
                st.rerun()
            if st.button('Chatbot for CFPB information', key='chatbot', use_container_width=True):
                if 'chatbot_open' not in st.session_state:
                    st.session_state.chatbot_open = False
                st.session_state.chatbot_open = not st.session_state.chatbot_open
            if st.button('Logout', key='logout', use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.page = 'Login'
                st.rerun()

            st.info("🎉 Join our Discord Community for Support and Updates. Help each other to solve the issues faster.")

            st.page_link("https://discord.gg/VJejVqUg3s", label="Discord Community", icon="🌎")

            # Embed the chatbot iframe with custom CSS
            if 'chatbot_open' in st.session_state and st.session_state.chatbot_open:
                components.html(
                    """
                    <style>
                    .chatbot-container {
                        width: 100%;
                        height: 400px;
                        overflow: hidden;
                        background: white;
                        border: 1px solid black;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    .chatbot-iframe {
                        width: 100%;
                        height: 100%;
                        border: none;
                        border-radius: 10px;
                    }
                    </style>
                    <div class="chatbot-container">
                        <iframe class="chatbot-iframe" src="https://app.fastbots.ai/embed/clxg1aa3802rrr9bct9iza0ks"></iframe>
                    </div>
                    """,
                    height=420  # Adjust this height as needed
                )

        elif st.session_state.page == 'Ticket Submission':

            ticket_submission(df)
            if st.button('Back to Home', key='home_from_submission', use_container_width=True):
                st.session_state.page = 'Home'
                st.rerun()
            if st.button('Logout', key='logout_submission', use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.page = 'Login'
                st.rerun()

        elif st.session_state.page == 'Ticket Information':
            # st_autorefresh(interval=5000, key="chat_refresh")

            ticket_information()
            if st.button('Back to Home', key='home_from_information', use_container_width=True):
                st.session_state.page = 'Home'
                st.rerun()
            if st.button('Logout', key='logout_information', use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.page = 'Login'
                st.rerun()


if __name__ == "__main__":
    tickets = load_tickets()
    create_tables()
    main()
