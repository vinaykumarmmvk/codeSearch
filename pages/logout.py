import streamlit as st 
import streamlit_authenticator as stauth 
import yaml
from yaml.loader import SafeLoader
from nav_js import navbar_loggedIn
from nav_js import setusrname
import time
from page_redirect import open_page
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedIn("profile")

headerstyle()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader) 
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.header("Log Out")
st.write("Are you sure you want to logout?")
if authenticator.logout("Yes"):
    setusrname("")
    open_page("/login")

if st.button("Cancel"):
    open_page("/todo_search")