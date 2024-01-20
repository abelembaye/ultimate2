# To run this app, open a terminal and run the following commands:
# pip install gcsfs (not needed with the below method; but there is another method that use gcsfs library)
import streamlit as st
# pip install gcsfs (not needed with the below method; but there is another method that use gcsfs library)
# import gcsfs
# import mysql.connector
#import pandas as pd
from sqlalchemy.sql import text # pip install SQLAlchemy
import sys
import os
import fn4authen_app2
# from fn4authen_app import check_password
# check_password()

st.session_state.username = st.session_state.username

# Initialize connection.
st.write("Welcom to my app")

# st.write(f"Session state before sql connections: {st.session_state}")

conn = st.connection('mysql', type='sql')

# st.write(f"Session state  after sql connections: {st.session_state}")

# Perform initial query.
df = conn.query('SELECT * from hw01;', ttl=0)

# Print initial fetching results:
# st.write(df)

# Get the username from the session state
# username = st.session_state.get("username", none)
if "username" in st.session_state:
    username = st.session_state["username"]
else:
    username = None
    st.write("you are in trouble because username is not in session state")


with st.form(key="fields_form2"):
    username = username.lower()
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
    # username = "aembaye" # entering manually works
    submit_button = st.form_submit_button(label="save")
    if submit_button:
        st.write(f"Username inside submit button: {username}")

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

# don't do the file below this line
# sys.exit()

# conda activate cvenv4st
# streamlit run ultimate_app2.py
