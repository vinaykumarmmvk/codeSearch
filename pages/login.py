import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
from yaml.loader import SafeLoader

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

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