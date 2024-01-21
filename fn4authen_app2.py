# Authenticator app; in streamlit the .streamlit/secrets.toml file must be entered manually in the cloud envt; username must be unique
# toml file can have sections and can store different secrets for different apps or parts of apps
# secret file or database are part of backend
# See more detail at:
# https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

import hmac  # pip install hmac
import streamlit as st


class Authenticator:
    def __init__(self, df):
        self.df = df

    def login_form(self):
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username without @uark.edu", key="username")
            st.text_input("Access code", type="password", key="password")
            st.form_submit_button("Log in", on_click=self.password_entered)

    def password_entered(self):
        """Checks whether a password entered by the user is correct."""
        username_lower = st.session_state["username"].lower()
        user_row = self.df[self.df['username'].str.lower() == username_lower]
        if not user_row.empty and user_row['password'].values[0] == st.session_state["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    def check_password(self):
        """Returns `True` if the user had a correct password."""
        if st.session_state.get("password_correct", False):
            return True

        # Show inputs for username + password.
        self.login_form()
        if "password_correct" in st.session_state:
            st.error("😕 User not known or password incorrect")
        return False


# if not Authenticator():
#     st.stop()

# Print the session state
# st.write(f"Session state after check_password: {st.session_state}")
# Main Streamlit app starts here
# st.write("Here goes your normal Streamlit app...")
# st.button("Click me")

