# Authenticator app; in streamlit the .streamlit/secrets.toml file must be entered manually in the cloud envt; username must be unique
# toml file can have sections and can store different secrets for different apps or parts of apps
# secret file or database are part of backend
# See more detail at:
# https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

import hmac  # pip install hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username without @uark.edu", key="username")
            st.text_input("Access code", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username_lower = st.session_state["username"].lower()
        if username_lower in (user.lower() for user in st.secrets["passwords"]) and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[username_lower],
        ):
            st.session_state["password_correct"] = True
            # Don't store the username or password.
            # del st.session_state["username"]
            del st.session_state["password"]

        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        # Print the session state
        # st.write(f"Session state in check_password: {st.session_state}")
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

# Print the session state
# st.write(f"Session state after check_password: {st.session_state}")
# Main Streamlit app starts here
# st.write("Here goes your normal Streamlit app...")
# st.button("Click me")
