import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

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