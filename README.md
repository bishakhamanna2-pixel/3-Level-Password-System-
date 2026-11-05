# 🔐 Three-Level Password System

A secure authentication system developed using **Python and Streamlit** that provides multiple layers of user verification. The system improves security by requiring users to successfully complete three authentication levels before access is granted.

## 📌 Project Overview

Traditional password-based authentication can be vulnerable if a user's password is compromised. This project implements a **Three-Level Password System** where a user must pass multiple verification stages.

### 🔑 Three Authentication Levels

**Level 1 — Username & Password Authentication**
The user enters their registered username and password. The system verifies the credentials stored in the database.

**Level 2 — OTP Verification**
After successful password authentication, an **OTP (One-Time Password)** is generated and used as an additional verification step.

**Level 3 — Face Recognition**
The system uses the device camera to capture and verify the user's face, providing an additional biometric security layer.

After successfully completing all three levels, the user is authenticated and granted access to the system.

## ✨ Features

* 👤 User Registration
* 🔑 Username and Password Login
* 🔢 OTP-based Verification
* 📷 Face Recognition Authentication
* 🗄️ User Data Storage
* 🛡️ Multi-Level Security
* 🖥️ Simple Streamlit User Interface
* 🚪 Secure Logout Option

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **OpenCV**
* **SQLite / Database**
* **OTP Generation**
* **Face Detection & Recognition**

## 📂 Project Structure

```text
3level pass sys/
│
├── app.py
├── database.py
├── otp.py
├── face.py
├── requirements.txt
└── README.md
```

### File Description

* `app.py` — Main Streamlit application and authentication flow.
* `database.py` — Handles user registration, login data, and database operations.
* `otp.py` — Handles OTP generation and verification.
* `face.py` — Handles camera access, face detection, and face verification.
* `requirements.txt` — Contains the Python packages required to run the project.

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔄 Authentication Workflow

```text
User Registration
       ↓
Username & Password
       ↓
OTP Verification
       ↓
Face Recognition
       ↓
Authentication Successful
       ↓
Access Granted
       ↓
Logout
```
<img width="634" height="235" alt="image" src="https://github.com/user-attachments/assets/65d8d999-e348-484e-a04e-77be5299f543" />


## 🔒 Security Purpose

The main purpose of this project is to demonstrate how **multi-factor authentication** can provide better security than relying only on a traditional password.

Even if one authentication factor is compromised, an unauthorized user must still pass the remaining verification levels.

## 🚀 Future Enhancements

* Password hashing and stronger encryption
* Improved face recognition accuracy
* OTP expiration mechanism
* Login attempt limitation
* Password recovery functionality
* Authentication history
* Improved user interface
* Cloud database integration

## 👩‍💻 Author

**Bishakha Manna**

## 📄 Project Type

Academic project demonstrating **multi-level authentication using Python, OTP verification, and face recognition**.
