import streamlit as st

from sqlalchemy.sql import text  # pip install SQLAlchemy

from fn4authen_app2 import Authenticator

# st.session_state.username = st.session_state.username


# Initialize connection.
# st.write("Welcom to my app")

# st.write(f"Session state before sql connections: {st.session_state}")

conn = st.connection('mysql', type='sql')

# st.write(f"Session state  after sql connections: {st.session_state}")

# Perform initial query.
df = conn.query('SELECT * from hw01;', ttl=0)

# Create an instance of Authenticator with df as an argument
authenticator = Authenticator(df)

# Now you can use the authenticator instance to call methods of the Authenticator class
if not authenticator.check_password():
    st.stop()

# Now you can use st.session_state.username without getting an error
st.session_state.username = st.session_state.username

if "username" in st.session_state:
    username = st.session_state["username"].lower()
else:
    username = None
    st.write("you are in trouble because username is not in session state")

with st.form(key="fields_form2"):
    user_row = df.loc[df['username'].str.lower() == username]
    st.write(f"user_row: {user_row}")
    if not user_row.empty:
        q1_default_val = user_row['q1'].values[0]
        q2_default_val = user_row['q2'].values[0]
    else:
        q1_default_val = None
        q2_default_val = None

    q1 = st.text_input("Enter some text", q1_default_val, key=1)
    q2 = st.text_input("Enter some text", q2_default_val, key=2)
    submit_button = st.form_submit_button(label="save")
    if submit_button:
        st.write(f"username inside submit button: {username}")

        with conn.session as s:
            sql = text(
                'UPDATE hw01 SET q1=:q1, q2=:q2 WHERE username=:username;')
            params = dict(q1=q1, q2=q2, username=username)
            result = s.execute(sql, params)
            s.commit()
            # Print the number of rows affected
            st.write(f"Rows affected: {result.rowcount}")
            s.close()

        st.write("q1 and q2 added to the database! and here is the table: ")
        df = conn.query('SELECT * from hw01;', ttl=0)
        st.write(df)
