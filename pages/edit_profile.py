import streamlit as st
import mysql.connector
import requests

from nav_bar import sidebar

from streamlit_modal import Modal

sidebar()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

modal = Modal(key="Demo Key",title="Verify password")
open_modal = st.button("Open")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        st.write("Please enter your current password:")
        current_password = st.text_input("Password", type="password") 
        #check from db if the password entered is correct
        #if password entered is correct close modal and allow user to make changes in profile
        #else show msg that password is wrong
        if st.button('Submit'):
            st.write("edit profile")
            

r = requests.get('http://localhost:8502', )

email = st.text_input("Email")
new_password = st.text_input("Password", type="password") 

password_repeat = st.text_input("Retype Password", type="password") 

specialization_proglang = st.multiselect( 'Please select programming language/s',
['java', 'c', 'cpp', 'cs', 'py', 'js'],[])

if st.button('Submit'):
    #validate email and password
	#check if email already exists or not
	#at least 1 specialized prog lang has to be selected
	#if validation fails redirect to same page
	#else redirect to search page
    st.write("Edit success")

modal_delete = Modal(key="Demo Key",title="Delete account")

if st.button('Delete'):
    modal_delete.open()

if modal_delete.is_open():
    with modal_delete.container():
        st.write("Are you sure you want to delete your account")
      	#check from db if the password entered is correct
        #if password entered is correct close modal and allow user to make changes in profile
        #else show msg that password is wrong
        if st.button('yes'):
            st.write("edit profile")
            st.write("account deleted successfully!")
        if st.button('No'):
            st.write("dosomething")