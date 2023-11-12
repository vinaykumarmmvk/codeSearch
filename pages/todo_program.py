import streamlit as st
import mysql.connector
import pandas as pd
import sys
from datetime import datetime
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import getusrname
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedIn("todo")

headerstyle()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)


username = getusrname()
#Retrieve user Id from username 

userId = (pd.read_sql("select user_id from users where user_name = '%s'"% (username), mydb))['user_id'][0]

cursor = mydb.cursor()
add_query = ("INSERT INTO fileDetails "
               "( file_name, file_description , user_id, extension_id, file_data, created_date) "
               "VALUES (%s, %s, %s, %s, %s, %s)")




filePath = ""
filename = ""
prog_content = ""

prog_description = ""
option = ""

#try catch to be added to check folder already exists
st.header("Add Program")
query_params = st.experimental_get_query_params()
prog_name = query_params.get("key1")[0]
prog_lang = query_params.get("key2")[0]

if prog_name is None:
   prog_name = ""

if prog_lang is None:
   prog_lang = ""

extId = ""

if prog_lang != "":
   match prog_lang:
      case "java":
         extId="1"

      case "c":
         extId="2"

      case "cpp":
         extId="3"

      case "cs":
         extId="4"

      case "js":
         extId="5"

      case "py":
         extId="6"

      case "php":
         extId="7"

with st.form(key='addprogform',clear_on_submit=True):
      prog_name = st.text_input("Enter program name", prog_name, disabled=True)
      prog_lang = st.text_input("Enter program name", prog_lang, disabled= True)
      prog_description = st.text_input("Description")

      #file content is the code of program name in the selected programming language.
      prog_content = st.text_area("Please enter code here","", height=400)

      submit_btn = st.form_submit_button("Add")

if prog_name is not '' and prog_lang is not '' :
   if submit_btn:
         #Remove white spaces from the program name entered
         prog_name = prog_name.replace(" ", "")

         #check if program name already exists
         df_file = pd.read_sql("select * from fileDetails where file_name = '%s' and extension_id = %s "% (prog_name, extId), mydb)
         
         #current date time is recorded as the program is added to a new file
         current_dateTime = datetime.now()

         prog_content_bin = prog_content.encode('UTF-8')

         if df_file.size > 0:
            st.warning("Data already added!")
            sys.exit()

         #update db tables with the added files
         add_data = (prog_name, prog_description, str(userId), str(extId), prog_content_bin, current_dateTime)
         cursor.execute(add_query, add_data)
         query = """Update searchData set result_exists = 1 where file_name = '%s' and extension_id = %s"""
         cursor.execute(query ,params=(prog_name, extId))
         mydb.commit()
         cursor.close()
         st.success("Code added successfully!")
         

else:
   st.error("Please enter Program Name/Program language")
   