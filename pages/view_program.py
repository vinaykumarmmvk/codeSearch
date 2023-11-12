import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_extras.switch_page_button import switch_page
from page_redirect import open_page
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
from nav_js import getusrname
import time
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
username = getusrname()

if username != "":
    navbar_loggedIn("search")

else:
    navbar_loggedOut("search")
    
headerstyle()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

query_params = st.experimental_get_query_params()
part_filename = query_params.get("key1")

st.header("View program "+part_filename[0])

whitespace = 7
progList = ["Java", "C", "C++", "C#", "JS", "Python", "php"]
tab1, tab2, tab3, tab4 ,tab5 ,tab6 ,tab7  = st.tabs([s.center(whitespace,"\u2001") for s in progList])

#READ file content inside the tab cond. 
#if file not found or empty keep tab empty
#user specalized with specific lang. show him with add or edit option

fname = part_filename[0]
extIds = [1,2,3,4,5,6,7]
fdata = []

for extId in extIds:
   df_file = pd.read_sql("select file_data from fileDetails where extension_id = %s and file_name = '%s'"% (str(extId),fname), mydb)
   if df_file.size != 0:
      df_data = df_file['file_data'][0].decode('UTF-8')
   else:
      df_data = ""
   fdata.append(df_data)

with tab1:
   st.header("Java")
   st.code(fdata[0], language='java')
   download_data = fdata[0]
   ext = ".java"
   st.download_button('Download', download_data, file_name=fname+ext)

with tab2:
   st.header("C")
   st.code(fdata[1], language='c')
   download_data = fdata[1]
   ext = ".c"
   st.download_button('Download', download_data, file_name=fname+ext)

with tab3:
   st.header("C++")
   st.code(fdata[2], language='c')
   download_data = fdata[2]
   ext = ".cpp"
   st.download_button('Download', download_data, file_name=fname+ext)

with tab4:
   st.header("C#")
   st.code(fdata[3], language='c')
   download_data = fdata[3]
   ext = ".cs"
   st.download_button('Download', download_data, file_name=fname+ext)

with tab5:
   st.header("JS")
   st.code(fdata[4], language='js')
   download_data = fdata[4]
   ext = ".js"
   st.download_button('Download', download_data, file_name=fname+ext)

with tab6:
   st.header("python")
   st.code(fdata[5], language='py')
   download_data = fdata[5]
   ext = ".py"
   st.download_button('Download', download_data, file_name=fname+ext)

with tab7:
   st.header("PHP")
   st.code(fdata[6], language='php')
   download_data = fdata[6]
   ext = ".php"
   st.download_button('Download', download_data, file_name=fname+ext)

if st.button("Edit"):
   open_page("/edit_program?key1="+fname)
