import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import mysql.connector
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

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.write("login success")
    authenticator.logout("Logout", "main") 
    if authentication_status:
        try:
            if authenticator.update_user_details(username, 'Update user details'):
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                newemail = config['credentials']['usernames'][username]['email']
                newname = config['credentials']['usernames'][username]['name']

                update_query = cursor.execute("Update users set user_fullname = '%s',email = '%s' where user_name = '%s'"%(newname, newemail, username))
                mydb.commit()
                
                st.success('Entries updated successfully')

        except Exception as e:
            st.error(e)