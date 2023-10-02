from datetime import datetime

import mysql.connector
import pandas as pd
import streamlit as st
from streamlit_javascript import st_javascript

from agstyler import PINLEFT, PRECISION_TWO, draw_grid

#from nav_bar import sidebar

#sidebar()

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

genre = st.radio(
    "Please select type of log/s",
    ('Search Page', 'OpenAI Search'))

if genre == 'Search Page':
    prog_name = st.text_input("Enter program name")

    option_ids = []
    options = st.multiselect( 'Please select programming language/s',
    ['java', 'c', 'cpp', 'cs', 'py', 'js', 'php'],[])

    res_exists = st.checkbox("Result exists")

    query = "Select * from searchData"
    flag = 0
    if prog_name is not '':
        if flag == 0:
            query = query + " WHERE searched_for like '%"+prog_name+"%'" 
            flag = 1
        else:
            query = query +" and searched_for like '%"+prog_name+"%'" 

    if res_exists is 'No':
        if flag == 0:
            query = query + " WHERE result_exists like '%"+res_exists+"%'" 
            flag = 1
        else:
            query = query +" and result_exists like '%"+res_exists+"%'" 

        
    if len(options) != 0 :
        if flag == 0:
            query = query + " WHERE extension_id IN (select extension_id from extension where extension_type LIKE '%s'" % (options[0])
            flag = 1
        else:
            query = query + " and extension_id IN (select extension_id from extension where extension_type LIKE '%s'" % (options[0])

        
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
   
    df_search = pd.read_sql(query, mydb)
            
    formatter = {
            'search_id': ('Index', PINLEFT),
            'searched_for': ('Searched for', {'width': 120}),
            'result_exists': ('Code ID', {'width': 80}),
            'extension_id': ('EXT ID', {'width': 80}),
            'search_date': ('Created date', {**PRECISION_TWO, 'width': 100})
    }
        
    if len(df_search) > 0:
        data = draw_grid(
                df_search.head(1000),
                formatter=formatter,
                fit_columns=True,
                selection='single',  # or 'single', or None
                use_checkbox='True',
                max_height = 500,
                wrap_text = True,
                auto_height = True,
            )
            
        if len(data.selected_rows) > 0:
            log_id = str(data.selected_rows[0]["search_id"])

        if st.button('View'):
            st.markdown("[share](/view_log?key1="+log_id+")")

        if st.button('Download'):
            st.write('download clicked') 

    mydb.close()

if genre == 'OpenAI Search':
    st.write("openAI SEARCH")
    search_description = st.text_input("Enter openAI Search description")

    query1= "Select * from fileDetails where file_name like 'OpenAI%' and extension_id = 8"
    
    if search_description is not '':
        query1 = query1+" and file_description like '%"+search_description+"%'"
        
    df = pd.read_sql(query1, mydb)

         
    formatter = {
            'file_name': ('File name', {'width': 120}),
            'file_description': ('Search description', {'width': 120}),
            'created_date': ('Searched date', {'width': 120})
    }
        
    if len(df) > 0:
        data = draw_grid(
                df.head(1000),
                formatter=formatter,
                fit_columns=True,
                selection='single',  # or 'single', or None
                use_checkbox='True',  # or False by default
                max_height=300
            )
            
        if len(data.selected_rows) > 0:
            file_id = str(data.selected_rows[0]["file_id"])
            st.markdown("[share](/view_ai_log?key1="+file_id+")")

        if st.button('Download'):
            st.write('download clicked') 

    mydb.close()
