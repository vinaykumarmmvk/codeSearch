#write about code search
#write about myself
#thesis work under Prof. Lano
import streamlit as st
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from streamlit.components.v1 import html
from nav_js import getusrname
from nav_js import headerstyle


st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")
time.sleep(1)
username = getusrname()

if username != "":
    navbar_loggedIn("about")

else:
    navbar_loggedOut("about")

headerstyle()

st.header("About us")

st.write("content goes here content goes here content goes here content goes here")
st.write("content goes here content goes here content goes here content goes here")
