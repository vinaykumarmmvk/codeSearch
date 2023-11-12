import streamlit as st
from nav_js import navbar_loggedIn
import time
import mysql.connector
import pandas as pd
from nav_js import getusrname
from page_redirect import open_page
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedIn("profile")

headerstyle()

username = getusrname()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

st.header("User Details")

if username is not None:
    query = "Select * from users where user_name is '%s"
    df = pd.read_sql("select * from users where user_name = '%s'"% (username), mydb)  

    st.write("User Name: "+username)
    st.write("Full name: "+df['user_fullname'][0])
    st.write("Email: "+df['email'][0])

    if st.button("Edit Details"):
        open_page("/edit_profile")

    if st.button("Change Password"):
        open_page("/updatePwd")
    #Display User details
    #Link/button to change user details/pwd 