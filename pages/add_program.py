import streamlit as st
import mysql.connector
import pandas as pd
import sys
from datetime import datetime
#from nav_bar import sidebar

#sidebar()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

#st.session_state['username']
username = "test"
#Retrieve user Id from username 
userId = (pd.read_sql("select user_id from users where user_name = '%s'"% (username), mydb))['user_id'][0]

#Retrieve the programming lang. the user is skilled/experienced 
df = pd.read_sql("select extension_type from extension where extension_id IN (select extension_id from userTodo where user_id = '%s')"% (userId), mydb)

cursor = mydb.cursor()
add_query = ("INSERT INTO fileDetails "
               "( file_name, file_description , user_id, extension_id, file_data, created_date) "
               "VALUES (%s, %s, %s, %s, %s, %s)")

skill_set = []
skill_setIds = []

for index in range(df['extension_type'].size):
    value = df['extension_type'][index]
    skill_set.append(value)

#drop down to select the prog lang list
#show prog list based on the skill set of the user
#should be able to add only if logged in has skill set
#same goes with the add screen


#READ file content inside the tab cond. 
#if file not found or empty keep tab empty
#user specalized with specific lang. show him with add or edit option
filePath = ""
filename = ""
prog_content = ""
prog_name = ""
prog_description = ""
option = ""

#try catch to be added to check folder already exists

if len(skill_set) != 0:
   with st.form(key='addprogform',clear_on_submit=True):
      prog_name = st.text_input("Enter program name")
      prog_description = st.text_input("Description")

      option = st.selectbox('Please Select Programming language to edit:', skill_set)

      #file content is the code of program name in the selected programming language.
      prog_content = st.text_area("Please enter code here","", height=400)

      submit_btn = st.form_submit_button("Add")

   if prog_name is not '' and len(option) != 0 :
      if submit_btn:
         #Remove white spaces from the program name entered
         prog_name = prog_name.replace(" ", "")

         #check if program name already exists
         df_file = pd.read_sql("select * from fileDetails where file_name = '%s'"% (prog_name), mydb)
         
         if df_file.size > 0:
            st.error("Program name already exists!")
            sys.exit()
         
         prog_content_bin = prog_content.encode('UTF-8')

         #fetch extension id from extension type
         df_extIds = pd.read_sql("select extension_id from extension where extension_type = '%s'"% (option), mydb)
         ext_id = df_extIds['extension_id'][0]
   
         #current date time is recorded as the program is added to a new file
         current_dateTime = datetime.now()

         #update db tables with the added files
         add_data = (prog_name, prog_description, str(userId), str(ext_id), prog_content_bin, current_dateTime)
         cursor.execute(add_query, add_data)
         mydb.commit()
         cursor.close()
         st.success("Code added successfully!")
         #after adding the code clear all the text fields and values

   else:
      st.error("Please enter Program Name")

else:
   #give hyperlink to todo screen to update skills
   st.write("Please update your skill set to add/edit program.")