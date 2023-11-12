import mysql.connector
import pandas as pd
import streamlit as st
from agstyler import PINLEFT, PRECISION_TWO, draw_grid
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import getusrname
from page_redirect import open_page
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedIn("todo")

headerstyle()

st.header("Todo list")

mydb = mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "1234",
       database = "codesearch"
  )

username = getusrname()
#Retrieve user Id from username 
userId = (pd.read_sql("select user_id from users where user_name = '%s'"% (username), mydb))['user_id'][0]
df = pd.read_sql("select extension_type from extension where extension_id IN (select extension_id from userTodo where user_id = '%s')"% (userId), mydb)

cursor = mydb.cursor()
add_query = ("INSERT INTO userTodo (user_id , extension_id) VALUES (%s, %s)")

skill_set = []

for index in range(df['extension_type'].size):
    value = df['extension_type'][index]
    skill_set.append(value)

options = ['java', 'c', 'cpp', 'cs', 'js', 'py','php']
options_selected = []
for i in range(len(skill_set)):
    for j in range(len(options)):
        if skill_set[i] == options[j]:
            options.remove(skill_set[i])
            break

options_selected = st.multiselect( 'Please select programming language/s', options,[])


if len(options_selected) != 0:
    if st.button("Add Skill"):
        skill_set.append(options_selected)

option_ids = []

for i in range(len(options_selected)):
        x = options_selected[i]
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

        add_data = (str(userId), str(option_ids[i]))
        cursor.execute(add_query, add_data)
        mydb.commit()

if len(skill_set)!=0:
    for i in range(len(skill_set)):    
        if i == 0:
            todo_query = "select * from searchData where result_exists = 0 and (extension_id  = (select extension_id from extension where extension_type like '%s')"% skill_set[i]
        else:
            todo_query = todo_query + " or extension_id  = (select extension_id from extension where extension_type like '%s')"% skill_set[i]
    todo_query = todo_query + ")"

    todo_set = pd.read_sql(todo_query, mydb)

    progList = []

    if len(todo_set) > 0:
        for x in range(len(todo_set)):
            match todo_set["extension_id"][x]:
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
            

        todo_set['PL'] = progList
        
        formatter = {
        'searched_for': ('Program Name', {'width': 80}),
        'PL': ('Prog lang', {'width': 50}),
        'search_date': ('Search date', {**PRECISION_TWO, 'width': 80})
        }
        data = draw_grid(
            todo_set.head(20),
            formatter=formatter,
            fit_columns=True,
            selection='single',  # or 'single', or None
            use_checkbox='True',  # or False by default
            max_height=300
        )
        
        if len(data.selected_rows) > 0:
            prog_name = data.selected_rows[0]["searched_for"]
            prog_lang = data.selected_rows[0]["PL"]
            open_page("../todo_program?key1="+prog_name+"&&key2="+prog_lang)

mydb.close()
#selected option inserted into the table and to skill_set 
#based on the skill set filter the todo list from the search table

