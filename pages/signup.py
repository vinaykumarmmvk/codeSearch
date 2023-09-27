import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import mysql.connector
import pandas as pd
import streamlit as st
import numpy as np

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

cursor = mydb.cursor()
add_data = ("INSERT INTO users "
               "( user_name, user_fullname , user_password, email) "
               "VALUES (%s, %s, %s, %s)")

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
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_name = st.text_input("Name")
    new_password = st.text_input("password", type="password")
    new_password_repeat = st.text_input("Repeat Password", type="password")
    
    if st.button('Register'):
        if authenticator.validator.validate_name(new_name):
            if authenticator.validator.validate_username(new_username):
                if authenticator.validator.validate_email(new_email):        
                    if len(new_email) and len(new_username) and len(new_name) and len(new_password) > 0:
                        if new_username not in authenticator.credentials['usernames']:
                            if new_password == new_password_repeat:
                                    new_password = stauth.Hasher([new_password]).generate()
                                    st.write(new_password)
                                    user_data = (new_username, new_name, new_password[0], new_email)
                                    cursor.execute(add_data, user_data)
                                    mydb.commit()
                                    
                                    record_to_add = dict(email=new_email,name=new_name, password=new_password[0])
                                    config["credentials"]['usernames'][new_username] = record_to_add

                                    with open('config.yaml', 'w') as file:
                                        yaml.dump(config, file, default_flow_style=False)

                                    st.success("data added successfully!")
                            else:
                                st.error('Passwords do not match')
                        else:
                            st.error('Username already taken')
                    else:
                        st.error('Please enter an email, username, name and password')
                else:
                    st.error("Enter valid email")
            else:
                 st.error("enter valid username")
        else:
             st.error("enter valid name")


except Exception as e:
    st.error(e)