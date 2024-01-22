import streamlit as st
import sqlalchemy.sql

# conn = st.connection('mysql', type='sql')
st.experimental_connection

# Perform query.
df = conn.query('SELECT * from hw01;', ttl=0)

st.write(df)
