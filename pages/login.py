import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
from yaml.loader import SafeLoader
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
from nav_js import setusrname
from nav_js import getusrname
import time
import requests
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

username = getusrname()

if username != "":
    navbar_loggedIn("login")

else:
    navbar_loggedOut("login")

headerstyle()

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
    st.write("login success"+username)
    setusrname(username)

st.markdown("""
    <a href="/signup" target = "_self"> 
        Sign Up 
    </a>
""", unsafe_allow_html=True)

st.markdown("""
    <a href="/forgotPwd" target = "_self"> 
        Forgot Password 
    </a>
""", unsafe_allow_html=True)