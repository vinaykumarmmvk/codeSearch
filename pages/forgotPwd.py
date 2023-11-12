import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.mime.text import MIMEText
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
    username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
    if username_of_forgotten_password:
        st.write("email is"+email_of_forgotten_password+"  new rndm pwd: "+new_random_password)
        st.write("user name "+username_of_forgotten_password)
        with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
        
        email_sender= "manjunath.vinay2@gmail.com"
        email_receiver = email_of_forgotten_password
        subject = "Password recovery email"
        pwd = "mtxm mnsh xlhz wfrk"
        bodyContent = "Please find your password recovery "+new_random_password

        try:
            msg = MIMEText(bodyContent)
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = subject

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_sender, pwd)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()

            st.success('Email sent successfully!')
        except Exception as e:
            st.error(f"Error log in mail : {e}")
    
        st.success('New password to be sent securely')
        # Random password should be transferred to user securely
    else:
        if username_of_forgotten_password == None:
             st.warning("Please enter Username")
        else:
            st.error('Username not found')
except Exception as e:
    st.error(e)

st.markdown("""
    <a href="/forgotUsrname" target = "_self"> 
        Forgot Username 
    </a>
""", unsafe_allow_html=True)