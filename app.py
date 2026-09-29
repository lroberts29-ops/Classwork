import streamlit as st
from auth import check_auth, show_logout_button

# Initialize the authenticated flag the first time the app runs in a session.
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Initialize the username the first time the app runs in a session.
if "username" not in st.session_state:
    st.session_state["username"] = None

# If the visitor is already authenticated, skip the form and show a welcome message.
if st.session_state["authenticated"] == True:
    st.success(f"Logged in as {st.session_state['username']}.")
    correct_username = st.secrets["credentials"]["username"]
    st.write("You are logged in - Welcome!", correct_username)
else:
    # st.form groups the two inputs and the submit button so the app only reruns once, on submit.
    login_form = st.form("login_form")

    # Add the username field inside the form.
    entered_username = login_form.text_input("Username")

    # Add the password field inside the form. type="password" masks the characters as they are typed.
    entered_password = login_form.text_input("Password", type="password")

    # Add the submit button inside the form.
    submitted = login_form.form_submit_button("Log in")

    # Only check credentials after the form has been submitted.
    if submitted == True:
        # Read the correct username out of secrets.toml.
        correct_username = st.secrets["credentials"]["username"]
        # Read the correct password out of secrets.toml.
        correct_password = st.secrets["credentials"]["password"]

        # Compare the entered credentials against the ones in secrets.toml.
        username_matches = entered_username == correct_username
        password_matches = entered_password == correct_password

        # Both fields must match before access is granted.
        if username_matches and password_matches:
            st.session_state["authenticated"] = True
            st.session_state["username"] = entered_username
            # Rerun so the welcome message replaces the form immediately.
            st.rerun()
        else:
            st.error("Incorrect username or password.")
