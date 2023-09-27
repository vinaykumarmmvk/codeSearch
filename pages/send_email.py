import streamlit as st
import mysql.connector
import requests

from nav_bar import sidebar

sidebar()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

r = requests.get('http://localhost:8502', )

prog_name = st.text_input("Email")

if st.button('Send Email'):
    #validate entered email, if it exists in db
    #if exists send password recovery link email
 	st.write("Email sent successfully")

