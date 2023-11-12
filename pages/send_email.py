import streamlit as st
import mysql.connector
import requests
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedOut()

email_id = st.text_input("Email")

if st.button('Send Email'):
    #validate entered email, if it exists in db
    #if exists send password recovery link email
 	st.write("Email sent successfully")

