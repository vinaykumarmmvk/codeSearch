import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
from yaml.loader import SafeLoader
import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

cursor = mydb.cursor()

# login and password change page using streamlit authentication

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.write("login success")
    authenticator.logout("Logout", "sidebar")

    try:
        if authenticator.reset_password(username, 'Reset password'):
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            
            newpwd = config['credentials']['usernames'][username]['password']
            update_query = cursor.execute("Update users set user_password = '%s' where user_name = '%s'"%( newpwd, username))
            mydb.commit()
            cursor.close()

            st.success('Password modified successfully')

    except Exception as e:
        st.error(e)