import streamlit as st
import sqlalchemy

conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from hw01;', ttl=0)

st.write(df)
