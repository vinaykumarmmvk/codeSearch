import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import mysql.connector
import pandas as pd
import streamlit as st
import numpy as np


with open('configtest.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.write(config["credentials"]['usernames'])

record_to_add = dict(email='lisa@test.com',name='Lisa', password='abc')
config["credentials"]['usernames']['lisa'] = record_to_add
  
with open('configtest.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
    

 