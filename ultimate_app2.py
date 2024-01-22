import streamlit as st
# import mysqlclient
# import pymysql
# pymysql.install_as_MySQLdb()

conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from hw01;')

st.write(df)
