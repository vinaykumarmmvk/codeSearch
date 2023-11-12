import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import mysql.connector
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import getusrname
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedIn("profile")

headerstyle()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

cursor = mydb.cursor()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

username = getusrname()

if username is not None:
        try:
            if authenticator.update_user_details(username, 'Edit user details'):
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                newemail = config['credentials']['usernames'][username]['email']
                newname = config['credentials']['usernames'][username]['name']

                update_query = cursor.execute("Update users set user_fullname = '%s',email = '%s' where user_name = '%s'"%(newname, newemail, username))
                mydb.commit()
                
                st.success('Entries updated successfully')

        except Exception as e:
            st.error(e)    