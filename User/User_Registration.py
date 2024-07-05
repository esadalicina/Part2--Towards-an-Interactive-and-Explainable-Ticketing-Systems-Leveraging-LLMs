from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import smtplib
import ssl
import uuid
import time
import bcrypt
import sqlite3
import certifi

# Initialize SQLite database connection


def create_tables():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()


    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT,
            email_confirmed INTEGER,
            confirmation_token TEXT
        )
    ''')
    conn.commit()

    c.execute('''
        CREATE TABLE IF NOT EXISTS email_confirmations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            token TEXT UNIQUE
        )
    ''')
    conn.commit()

    c.close()
    conn.close()


def send_confirmation_email(email, token):

    sender_email = "cfpb.helpdesk@gmail.com"  # Replace with your Gmail address
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Email Confirmation ✅"
    message["From"] = sender_email
    message["To"] = receiver_email

    confirmation_link = f"http://192.168.178.78:8502/?page=Confirm_Email&token={token}"
    text = f"Please confirm your email by clicking the link below:\n\n{confirmation_link}"
    part1 = MIMEText(text, "plain")

    # HTML version with button
    html = f"""
        <html>
        <body>
            <p>Please confirm your email by clicking the button below 😀</p>
            <a href="{confirmation_link}" style="
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;">
                Confirm Email
            </a>
        </body>
        </html>
        """
    part2 = MIMEText(html, "html")

    # Attach parts into message container
    message.attach(part1)
    message.attach(part2)

    try:
        context = ssl.create_default_context(cafile=certifi.where())
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, 'pbfc gvpl atax gfge')  # Use the app password here
            server.sendmail(sender_email, receiver_email, message.as_string())

        st.success('Registration successful! Please check your email to confirm your account.', icon="✅")

    except Exception as e:
        st.error(f"Error sending confirmation email: {e}", icon="🚨")


def get_email(username):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()

    c.execute('SELECT email FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if result:
        email = result[0]  # Extract the email from the tuple
        return email
    else:
        return None




def add_user(full_name, username, email, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        confirmation_token = str(uuid.uuid4())
        c.execute('''
                   INSERT INTO email_confirmations (email, token)
                   VALUES (?, ?)
               ''', (email, confirmation_token))
        conn.commit()

        c.execute('''
               INSERT INTO users (full_name, username, email, password, confirmation_token)
               VALUES (?, ?, ?, ?, ?)
           ''', (full_name, username, email, hashed_password, confirmation_token))
        conn.commit()

        send_confirmation_email(email, confirmation_token)

        c.close()
        conn.close()

        return True
    except sqlite3.IntegrityError as e:
        st.error(f"Database error: {e}")
        return False
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return False


def confirm_email(token):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()

    c.execute('SELECT email FROM email_confirmations WHERE token = ?', (token,))
    result = c.fetchone()
    if result:
        email = result[0]
        c.execute('UPDATE users SET email_confirmed = 1 WHERE email = ?', (email,))
        c.execute('DELETE FROM email_confirmations WHERE token = ?', (token,))
        conn.commit()

        c.close()
        conn.close()
        return True
    return False




def check_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()


    c.execute('SELECT password, email_confirmed FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    if result:
        hashed_password, email_confirmed = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            if email_confirmed:
                return True
            else:
                st.error("Please confirm your email before logging in.")
                return False
    return False



def email_confirmation_page(token):

    st.header("Email Confirmation")
    if confirm_email(token):
        st.success("Email confirmed! You can now log in.", icon="🎉")
        st.query_params.clear()
    else:
        st.error("Invalid or expired token.", icon="🚨")


def registration_page():

    st.header("User Registration")
    full_name = st.text_input("Full Name")
    username = st.text_input("Username", key="username1")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", key="password1")

    if st.button("Login", key='login2', use_container_width=True):
        st.session_state.page = 'Login'
        st.rerun()

    if st.button("Register", use_container_width=True):
        if full_name and username and email and password:
            try:
                add_user(full_name, username, email, password)
                time.sleep(5)
                st.session_state.page = 'Login'
                st.rerun()
            except sqlite3.IntegrityError:
                error = st.error("Username or Email already exists.", icon="🚨")
                time.sleep(2)
                error.empty()
        else:
            er = st.error("Please fill out all fields.", icon="🚨")
            time.sleep(2)
            er.empty()
    return username, email
