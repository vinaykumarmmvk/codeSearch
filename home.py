import streamlit as st
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
from yaml.loader import SafeLoader
import requests
from pages import aboutus

from streamlit import session_state as state
from streamlit.components.v1 import html
from streamlit_javascript import st_javascript
import re
import code
import socket
from json import loads as JSON
from nav_js import getusrname
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)

username = getusrname()

if username != "":
    navbar_loggedIn("home")

else:
    navbar_loggedOut("home")

headerstyle()

st.header("Code Search for Algorithms")
st.write("Python website using Streamlit framework to show,download and update ")
st.write("the code of various algorithms indifferent programming languages like Java, C, C++, C#,Python and JavaScript.")
st.write("The website has search algorithm page, view algorithmpage, login page, signup page, todo page, search log pageand various other pages.")