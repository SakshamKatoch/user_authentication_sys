import streamlit as st

from database import create_database
from auth import register_user, login_user


# Create database when the app starts
create_database()


# Page configuration
st.set_page_config(
    page_title="User Authentication System",
    page_icon="🔐",
    layout="centered"
)


# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- LOGIN PAGE ----------------

def login_page():
    st.title("🔐 User Authentication System")
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login", use_container_width=True):

        if not email or not password:
            st.warning("Please enter both email and password.")
            return

        success, user = login_user(email, password)

        if success:
            st.session_state.logged_in = True
            st.session_state.user = user

            st.success("Login successful!")
            st.rerun()

        else:
            st.error("Invalid email or password.")


# ---------------- REGISTER PAGE ----------------

def register_page():
    st.title("🔐 User Authentication System")
    st.subheader("Create an Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register", use_container_width=True):

        if not username or not email or not password:
            st.warning("Please fill in all fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        if len(password) < 6:
            st.warning("Password must contain at least 6 characters.")
            return

        success, message = register_user(
            username,
            email,
            password
        )

        if success:
            st.success(message)
        else:
            st.error(message)


# ---------------- DASHBOARD ----------------

def dashboard():
    user = st.session_state.user

    user_id = user[0]
    username = user[1]
    email = user[2]
    role = user[4]

    st.title("🏠 Dashboard")

    st.success(f"Welcome, {username}!")

    st.write(f"**User ID:** {user_id}")
    st.write(f"**Username:** {username}")
    st.write(f"**Email:** {email}")
    st.write(f"**Role:** {role}")

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# ---------------- MAIN APP ----------------

if st.session_state.logged_in:

    dashboard()

else:

    page = st.radio(
        "Select",
        ["Login", "Register"],
        horizontal=True
    )

    if page == "Login":
        login_page()

    else:
        register_page()