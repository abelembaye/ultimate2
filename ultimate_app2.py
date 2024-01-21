import streamlit as st

conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from hw01;', ttl=600)

st.write(df)
