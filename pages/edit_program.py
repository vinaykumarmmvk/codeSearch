import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime
from page_redirect import open_page
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import getusrname
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedIn("search")
username = getusrname()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

query_params = st.experimental_get_query_params()
part_filename = query_params.get("key1")

headerstyle()

#Retrieve user Id from username 
#file name should be unique in filedetails table
userId = (pd.read_sql("select user_id from users where user_name = '%s'"% (username), mydb))['user_id'][0]
df = pd.read_sql("select extension_type from extension where extension_id IN (select extension_id from userTodo where user_id = '%s')"% (userId), mydb)


skill_set = []

cursor = mydb.cursor()
add_query = ("INSERT INTO fileEditDetails "
               "( file_id, edit_description , user_id, edited_date) "
               "VALUES (%s, %s, %s, %s)")

addfile_query = ("INSERT INTO fileDetails "
               "( file_name, file_description , user_id, extension_id, file_data, created_date) "
               "VALUES (%s, %s, %s, %s, %s, %s)")

for index in range(df['extension_type'].size):
    value = df['extension_type'][index]
    skill_set.append(value)

fname = part_filename[0]
st.header("Edit Program"+part_filename[0])

if st.button('Cancel'):
 open_page("../view_program?key1="+fname)

#drop down to select the prog lang list
#show prog list based on the skill set of the user
#should be able to edit only if logged in and has skill set
#skill set condition to be added - pending
#same goes with the add screen

progList = ["C", "C++", "C#","Java","JS","PHP","Python"]

option = st.selectbox('Please Select Programming language to edit:', skill_set)
st.write('You selected:', option)

editDescription = st.text_input("Please enter edit description")
#READ file content inside the tab cond. 
#if file not found or empty keep tab empty
#user specalized with specific lang. show him with add or edit option


extId = ""

match option:
   case "java":
      st.subheader("Java")
      extId="1"

   case "c":
      st.subheader("C")
      extId="2"

   case "cpp":
      st.subheader("C++")
      extId="3"

   case "cs":
      st.subheader("C#")
      extId="4"

   case "js":
      st.subheader("JS")
      extId="5"

   case "py":
      st.subheader("Python")
      extId="6"

   case "php":
      st.subheader("PHP")
      extId="7"

try:
   df_file = pd.read_sql("select file_data from fileDetails where extension_id = %s and file_name = '%s'"% (extId, fname), mydb)
   if df_file.size != 0:
      df_data = df_file['file_data'][0].decode('UTF-8')#returns str type
   else:
      df_data = ""

   prog_content = st.text_area("Edit", df_data, height=400)


except Exception as e:
            prog_content = st.text_area("Edit","", height=400)
            st.error(f"Error log : {e}")

if st.button("Submit"):
   if editDescription != '':
      #once submit update the c,c++,java... files with the changed content
      #open file, write changes

      current_dateTime = datetime.now()

      prog_content_bin = prog_content.encode('UTF-8')
      
      #fileId = we get from filename and extensionid
      try:
         fileId = (pd.read_sql("select file_id from fileDetails where file_name = '%s' and extension_id = '%s'"% (fname,extId), mydb))['file_id'][0]
         if fileId > 0:
              #update file data
              query = """Update fileDetails set file_data = %s where file_id = %s"""
              cursor.execute(query ,params=(prog_content_bin, str(fileId)))
              st.success("File updated")

      except Exception as e:
            
            #create an entry in fileDetails and then fetch fileid
            addfile_data = (fname, editDescription, str(userId), extId, prog_content_bin ,current_dateTime)
            cursor.execute(addfile_query, addfile_data)
            fileId = (pd.read_sql("select file_id from fileDetails where file_name = '%s' and extension_id = '%s'"% (fname,extId), mydb))['file_id'][0]
            st.success("file created")
            st.error(f"Error log : {e}")
      
      
      add_data = (str(fileId), editDescription, str(userId), current_dateTime)
      cursor.execute(add_query, add_data)
      mydb.commit()
      cursor.close()

      st.success("Code updated successfully!")

   else:
      st.error("Please enter file description")