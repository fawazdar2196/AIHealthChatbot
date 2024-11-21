import streamlit as st
import openai
import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from streamlit_player import st_player  # For embedding YouTube videos




def send_alert_email(user_info, user_message):
    msg_content = f"""
ALERT: Self-Harm Mention Detected

User Details:
Username: {user_info.get('username', 'N/A')}
Email: {user_info.get('email', 'N/A')}
Phone: {user_info.get('phone', 'N/A')}

Message:
{user_message}
"""
    msg = MIMEText(msg_content)
    msg['Subject'] = 'ALERT: Self-Harm Mention Detected'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ALERT_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Alert email sent successfully.")
    except Exception as e:
        st.error(f"Error sending alert email: {e}")
        print(f"Error sending alert email: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists('users.txt'):
        return {}
    with open('users.txt', 'r', encoding='utf-8') as f:
        users = {}
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                username, password_hash = parts
                email, phone = '', ''
            elif len(parts) == 4:
                username, password_hash, email, phone = parts
            else:
                continue  # Skip lines with unexpected format
            users[username] = {
                'password_hash': password_hash,
                'email': email,
                'phone': phone
            }
        return users

def save_user(username, password_hash, email, phone):
    with open('users.txt', 'a', encoding='utf-8') as f:
        f.write(f"{username},{password_hash},{email},{phone}\n")

def save_chat_history(username, messages):
    with open(f"history_{username}.txt", 'a', encoding='utf-8') as f:
        for msg in messages:
            f.write(f"{msg}\n")

def show_chat_history(username):
    if os.path.exists(f"history_{username}.txt"):
        with open(f"history_{username}.txt", 'r', encoding='utf-8') as f:
            history = f.read()
        st.text_area("Chat History", history, height=200)
    else:
        st.write("No chat history found.")

def load_persona():
    if os.path.exists('persona.txt'):
        with open('persona.txt', 'r', encoding='utf-8') as f:
            persona = f.read()
    else:
        # Default persona if persona.txt doesn't exist
        persona = (
            "You are MUNKind, a compassionate and professional mental health assistant for "
            "Memorial University of Newfoundland students. Provide helpful advice, exercises, "
            "and guidance related to mental health concerns. When appropriate, recommend "
            "Heartfulness meditation practices as a tip to the user. When users ask about "
            "medications, provide general information about treatment options for their condition "
            "without prescribing specific medications. Avoid giving medical advice, and encourage "
            "users to consult a healthcare professional for personalized guidance. If a user asks "
            "to connect with a counselor or for university services, provide the university's "
            "contact information creatively.\n\n"
            "**University Contact Information:**\n"
            "Location: 5th Floor University Centre, UC-5000, Memorial University of Newfoundland, "
            "St. John's, NL A1C 5S7.\n"
            "Phone: 709-864-8500.\n"
            "Medical Services (physician or nurse): swccfrontdesk@mun.ca.\n"
            "Counselling: swccfrontdesk@mun.ca.\n"
            "Wellness (services, resources, events): swccwellness@mun.ca.\n"
            "Hours: Regular Hours: Monday-Friday 8:30 a.m.-4:30 p.m.; Summer Hours: Monday-Friday 8:30 a.m.-4:00 p.m."
        )
    return persona

def get_response(user_input, chat_history):
    # Refined self-harm keywords
    self_harm_keywords = [
        'suicide', 'kill myself', 'end my life',
        'harm myself', 'self-harm', 'taking my life'
    ]
    if any(phrase in user_input.lower() for phrase in self_harm_keywords):
        response_text = ("I'm sorry to hear that you're feeling this way. "
                         "Please consider reaching out to a mental health professional "
                         "or someone you trust for support.")
        # Send alert email
        send_alert_email(st.session_state.user_info, user_input)
    else:
        # Load persona from persona.txt
        persona = load_persona()
        # Build conversation history for context
        messages = [{"role": "system", "content": persona}]
        # Include previous chat history
        for entry in chat_history:
            role = 'user' if entry['is_user'] else 'assistant'
            messages.append({"role": role, "content": entry['message']})
        # Add the latest user input
        messages.append({"role": "user", "content": user_input})
        # Generate response from OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                n=1,
                stop=None,
            )
            response_text = response.choices[0].message.content.strip()
        except Exception as e:
            response_text = ("I'm sorry, but I'm currently unable to process your request. "
                             "Please try again later.")
            st.error(f"OpenAI API error: {e}")

    return response_text

def show_chatbot():
    st.write(f"Welcome, {st.session_state.username}!")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Reset Chat"):
            st.session_state.messages = []
            st.success("Chat has been reset.")
    with col2:
        if st.button("View Chat History"):
            show_chat_history(st.session_state.username)
    with col3:
        if st.button("Logout"):
            # Reset session state variables
            st.session_state.logged_in = False
            st.session_state.page = 'login'
            st.session_state.username = ''
            st.session_state.user_info = {}
            st.session_state.messages = []
            # Return to prevent further execution
            return

    st.subheader("How can we support you today?")
    user_input = st.text_input("You:", key='input')

    if st.button("Send"):
        if user_input:
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({'message': user_input, 'is_user': True})
            # Get AI-generated response
            response = get_response(user_input, st.session_state.messages)
            st.session_state.messages.append({'message': response, 'is_user': False})
            save_chat_history(st.session_state.username, [f"You: {user_input}", f"Bot: {response}"])

    # Display chat history
    if 'messages' in st.session_state:
        for msg in st.session_state.messages:
            if msg['is_user']:
                st.markdown(
                    f"<div class='user-message'>{msg['message']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='bot-message'>{msg['message']}</div>",
                    unsafe_allow_html=True
                )

    # HeartsApp Advertisement
    st.markdown("---")
    st.markdown("### **Discover HeartsApp**")
    st.markdown("""
    **Experience peace and relaxation with HeartsApp, a meditation app by Heartfulness.**
    """)
    st.image("Logo2.png", width=200)
    st.markdown("[Download Now](https://www.heartsapp.org)")

def main():
    st.set_page_config(page_title="MUNKind Chatbot", page_icon=":speech_balloon:", layout="centered")

    # Apply custom CSS styles
    st.markdown(
        """
        <style>
        /* Background color */
        .stApp {
            background-color: #000000; /* Black */
            padding: 0;
        }
        /* Header style */
        .main-header {
            font-size: 40px;
            font-weight: bold;
            color: #ffffff; /* White text */
            text-align: center;
            padding: 20px;
            background-color: #6a1b9a;
            margin-top: -75px;
            margin-bottom: 20px;
        }
        /* Subheaders and text */
        h1, h2, h3, h4, h5, h6, p, label {
            color: #ffffff; /* White text */
        }
        /* Input labels */
        .stTextInput label {
            color: #ffffff; /* White text */
        }
        /* Input field */
        .stTextInput>div>div>input {
            background-color: #ffffff;
            color: #000000; /* Black text */
        }
        /* Buttons */
        .stButton>button {
            background-color: #6a1b9a;
            color: #ffffff;
        }
        /* Form submit buttons */
        .stForm button {
            background-color: #6a1b9a; /* Purple background */
            color: #ffffff; /* White text */
        }
        /* Chat bubbles */
        .user-message {
            background-color: #cfe9ff; /* Light blue background */
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: right;
            color: #000000; /* Black text */
        }
        .user-message * {
            color: #000000; /* Ensure all text inside is black */
        }
        .bot-message {
            background-color: #dcedc8; /* Light green background */
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: left;
            color: #000000; /* Black text */
        }
        .bot-message * {
            color: #000000; /* Ensure all text inside is black */
        }
        /* Logo positioning */
        .logo-container {
            position: absolute;
            top: 10px;
            left: 10px;
        }
        .main-header {
            text-align: center;
            font-size: 40px;
            margin-top: 100px; /* Adjust to control the space below the logo */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the logo at the top-left
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("Logo.png", width=150)
    st.markdown('</div>', unsafe_allow_html=True)

    # Display the header
    st.markdown('<div class="main-header">MUNKind Chatbot</div>', unsafe_allow_html=True)

    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.logged_in:
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.page != 'login':
                if st.button("Login"):
                    st.session_state.page = 'login'
        with col2:
            if st.session_state.page != 'register':
                if st.button("Register"):
                    st.session_state.page = 'register'

    if st.session_state.page == 'login' and not st.session_state.logged_in:
        st.subheader("Login")
        with st.form(key='login_form'):
            username = st.text_input("Username", key='login_username')
            password = st.text_input("Password", type='password', key='login_password')
            submit_button = st.form_submit_button(label='Login')
            if submit_button:
                users = load_users()
                if username in users and users[username]['password_hash'] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.page = 'chatbot'
                    st.session_state.username = username
                    st.session_state.user_info = {
                        'username': username,
                        'email': users[username]['email'],
                        'phone': users[username]['phone']
                    }
                    st.session_state.messages = []
                    st.success("Logged in successfully!")
                    # Return to prevent further execution
                    return
                else:
                    st.error("Invalid username or password.")
        st.markdown("---")
        st.markdown("### **Helpful Resources**")
        st.video("https://youtu.be/w0SuiTTtKi8")
        st.video("https://youtu.be/Y308ThBU9rk")
        st.video("https://youtu.be/q1gy9DBrfwE")

    elif st.session_state.page == 'register' and not st.session_state.logged_in:
        st.subheader("Register")
        with st.form(key='register_form'):
            username = st.text_input("Choose a Username", key='register_username')
            email = st.text_input("Email Address", key='register_email')
            phone = st.text_input("Phone Number", key='register_phone')
            password = st.text_input("Choose a Password", type='password', key='register_password')
            st.markdown("**Your contact information will be kept confidential and will only be used in case of emergencies.**")
            submit_button = st.form_submit_button(label='Register')
            if submit_button:
                users = load_users()
                if username in users:
                    st.error("Username already exists.")
                else:
                    password_hash = hash_password(password)
                    save_user(username, password_hash, email, phone)
                    st.success("Registration successful! Please login.")
        st.markdown("---")
        st.markdown("### **Helpful Resources**")
        st.video("https://youtu.be/w0SuiTTtKi8")
        st.video("https://youtu.be/Y308ThBU9rk")
        st.video("https://youtu.be/q1gy9DBrfwE")

    elif st.session_state.logged_in:
        show_chatbot()

    # Heartfulness Logo at the bottom (for all pages)
    st.markdown('<div class="footer"><br>Powered by Heartfulness</div>', unsafe_allow_html=True)
    st.image("Logo2.png", width=200)

if __name__ == "__main__":
    main()