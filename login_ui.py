import streamlit as st
from authen import authenticate
import mysql.connector

from pages import support_dashboard
from pages import client_dashboard



salt = "random_salt_values"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abbivimi@7",
    database="user_management"
)


st.title("Client Query Management")



if 'user' not in st.session_state:
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        user = authenticate(username, password, conn, salt)
        if user:
            st.session_state['user'] = user
            st.success(f"Welcome {user['username']}! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password")
else:
    user = st.session_state['user']


    if user['role'] == 'support':
        support_dashboard.show_dashboard()   
    elif user['role'] == 'client':
        client_dashboard.show()  



  
