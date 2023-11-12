import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedOut("login")

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

try:
    username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username('Forgot username')
    if username_of_forgotten_username:
        st.success('Username to be sent securely')
        st.write("username "+username_of_forgotten_username)
        st.write("email of forgot user "+email_of_forgotten_username)
        
        # Username should be transferred to user securely
    else:
        if len(email_of_forgotten_username) == 0:
             st.warning("Please enter Email")
        else:
            st.error('Email not found')
except Exception as e:
    st.error(e)