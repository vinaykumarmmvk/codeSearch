from datetime import datetime

import mysql.connector
import pandas as pd
import streamlit as st
import numpy as np
from streamlit_javascript import st_javascript

from agstyler import PINLEFT, PRECISION_TWO, draw_grid
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from page_redirect import open_page
from nav_js import getusrname
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)

username = getusrname()
st.write(username)
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
st.header("Search page")
cursor = mydb.cursor()
add_data = ("INSERT INTO searchData "
               "( searched_for, result_exists , extension_id, search_date) "
               "VALUES (%s, %s, %s, %s)")


result_exists = 0

#options_id fetch id from table of resp. prog. lang
option_ids = []

@st.cache_data
def bind_socket(prog_name1, result_exists1, current_dateTime1):
    # This function will only be run the first time it's called
       
    for x in option_ids:
            if len(option_ids) > 0 :
                search_data = (prog_name1, result_exists1, str(x), current_dateTime1)
                cursor.execute(add_data, search_data)
                mydb.commit()

prog_name = st.text_input("Enter program name")

options = st.multiselect( 'Please select programming language/s',
['java', 'c', 'cpp', 'cs', 'py', 'js', 'php'],[])

current_dateTime = datetime.now()

if prog_name is not '' and len(options) != 0 :
    query="SELECT * FROM fileDetails WHERE file_name LIKE '%"+prog_name+"%'" +" and extension_id IN (select extension_id from extension where extension_type LIKE '%s'" % (options[0])

    for x in options:
        if len(options) > 0 :
            query =  query+" OR extension_type LIKE '%s'" % (x)
            match x:
                case "java":
                    option_ids.append(1)

                case "c":
                    option_ids.append(2)

                case "cpp":
                    option_ids.append(3)

                case "cs":
                    option_ids.append(4)

                case "js":
                    option_ids.append(5)

                case "py":
                    option_ids.append(6)

                case "php":
                    option_ids.append(7)

    query = query + ")"
    
    df = pd.read_sql(query, mydb)
    progList = []
    if len(df) > 0:
        for x in range(len(df)):
            match df["extension_id"][x]:
                case 1:
                    progList.append("java")

                case 2:
                    progList.append("c")

                case 3:
                    progList.append("cpp")

                case 4:
                    progList.append("cs")

                case 5:
                    progList.append("js")

                case 6:
                    progList.append("py")

                case 7:
                    progList.append("php")
            

    df['PL'] = progList

    formatter = {
        'file_name': ('File Name', {'width': 120}),
        'PL': ('Prog lang', {'width': 100}),
        'created_date': ('Created date', {**PRECISION_TWO, 'width': 100})
    }
    
    if len(df) > 0:
        result_exists = 1
        data = draw_grid(
            df.head(20),
            formatter=formatter,
            fit_columns=True,
            selection='single',  # or 'single', or None
            use_checkbox='True',  # or False by default
            max_height=300
        )
        
        if len(data.selected_rows) > 0:
            file_name = data.selected_rows[0]["file_name"]
            open_page("../view_program?key1="+file_name)
    else:
        st.warning("Result does not exists!")
        if st.button("OpenAI Search"):
            open_page("../openAITest")

    bind_socket(prog_name, result_exists, current_dateTime) 

cursor.close()
mydb.close()