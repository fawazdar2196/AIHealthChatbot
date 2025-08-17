# 🤖 MUNKind Chatbot Application  

A **compassionate mental health assistant** for students at **Memorial University of Newfoundland**.  
The chatbot provides **mental health advice**, tracks **chat history**, and can send **emergency alerts** to university mental health services if self-harm-related keywords are detected.  

---

## 📖 Overview  

The **MUNKind Chatbot** helps students by:  
- Offering **mental health guidance** through a friendly chat interface.  
- **Detecting emergencies** and alerting university services via email.  
- **Saving chat history** for each user.  
- Supporting a **custom chatbot personality** defined in `persona.txt`.  

---

## 📂 Files in the Project  

### 1. `app.py`  
The **main application file**, containing:  
- **Login/Register System**: Securely register with username, email, and phone number.  
- **Chat Interface**: Chat with the mental health assistant.  
- **Alert Email System**: Sends alerts when self-harm keywords are detected.  
- **Chat History**: Stores conversations per user.  

---

### 2. `users.txt`  
Stores registered user data in the format:  

- **username** → chosen username  
- **password_hash** → securely hashed password  
- **email** → user’s email  
- **phone** → user’s phone number  

---

### 3. `persona.txt`  
Defines the chatbot’s **personality and behavior**.  

- Provides guidelines for chatbot responses.  
- Suggests resources for students.  
- If missing, a **default persona** is used.  

---

### 4. `history_<username>.txt`  
Stores chat history for each user.  

- Format: Alternating user and chatbot messages.  
- Example:  

---

### 5. `Logo.png` & `Logo2.png`  
Logos used in the chatbot interface.  

---

## ⚙️ Installation Guide  

### ✅ Prerequisites  
- **Python 3.10+** installed on your system.  
- A **Gmail account** for email alerts (with **App Passwords enabled**).  

---

### 🔽 Steps to Install  
1. **Download or Clone this Repository**  
 ```bash
 git clone https://github.com/yourusername/MUNKind-Chatbot.git
 cd MUNKind-Chatbot
