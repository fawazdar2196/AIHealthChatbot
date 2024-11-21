MUNKind Chatbot Application

Overview

The MUNKind Chatbot is a compassionate mental health assistant for students at Memorial University of Newfoundland. This chatbot provides mental health advice, tracks chat history, and can alert university mental health services in case of emergency situations.

Files in the Project

1. app.py

This is the main file that contains:

Login/Register System: Enables users to register with their username, email, and phone number and securely log in.
Chat Interface: Allows users to chat with the chatbot and displays responses.
Alert Email System: Sends an email to alert mental health services if any self-harm-related keywords are detected.
Chat History: Saves user chats and enables users to view their chat history.

2. users.txt

This file stores user data in the following format:


username,password_hash,email,phone
username: User's chosen username.
password_hash: A hashed version of the user's password for security.
email: User's email address.
phone: User's phone number.

3. persona.txt

This file defines the chatbot's personality and behavior.

It contains guidelines about how the chatbot should respond to user queries and what resources it should suggest.
If this file is missing, a default persona is used.

4. history_<username>.txt

A separate file is created for each user to save their chat history.
Format: Alternating user and chatbot messages are stored.

5. Logo.png and Logo2.png

These image files are basically logos that are displayed on the chatbot interface.

Installation Guide

Prerequisites

Python 3.10 or higher installed on your system.
A Gmail account for email alerts. Enable App Passwords in your Gmail account settings.

Steps to Install

download the files to your local system.
Navigate to the project directory in your terminal:


Install the required dependencies:

pip install -r requirements.txt

Gmail Configuration
Replace the EMAIL_ADDRESS and EMAIL_PASSWORD in app.py with your Gmail address and App Password.
Replace ALERT_EMAIL with the email address where you want to receive alerts.

How to Run the Chatbot

Start the application:

And run: streamlit run app.py

Open the URL provided in the terminal (usually http://localhost:8501/).
Logging In and Registering
New users should first register by clicking the "Register" button.
Existing users can log in with their username and password.
Chat Interface
After logging in, users can start chatting with the chatbot.
Chat history is saved automatically and can be viewed using the "View Chat History" button.

Features

Login/Register System
Security: Passwords are securely hashed and stored in users.txt.
Chatbot Persona
The chatbot's personality is defined in persona.txt. Customize this file to change how the chatbot interacts with users.
Emergency Alert System
The chatbot detects self-harm-related keywords in user inputs and sends an alert email to the configured address.
Chat History
Saves each user's chat history in history_<username>.txt.
Videos and Resources
The app includes helpful YouTube videos about mental health and meditation.