import mysql.connector
import pandas as pd
import streamlit as st
from agstyler import PINLEFT, PRECISION_TWO, draw_grid

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
                st.write("java")
                option_ids.append(1)

            case "c":
                st.write("c")
                option_ids.append(2)

            case "cpp":
                st.write("cpp")
                option_ids.append(3)

            case "cs":
                st.write("cs")
                option_ids.append(4)

            case "js":
                st.write("js")
                option_ids.append(5)

            case "py":
                st.write("py")
                option_ids.append(6)

            case "php":
                st.write("php")
                option_ids.append(7)

        add_data = (str(userId), str(option_ids[i]))
        cursor.execute(add_query, add_data)
        mydb.commit()

st.write(skill_set)

for i in range(len(skill_set)):    
    if i == 0:
        todo_query = "select * from searchData where result_exists = 0 and (extension_id  = (select extension_id from extension where extension_type like '%s')"% skill_set[i]
    else:
        todo_query = todo_query + " or extension_id  = (select extension_id from extension where extension_type like '%s')"% skill_set[i]
todo_query = todo_query + ")"

todo_set = pd.read_sql(todo_query, mydb)
st.write(todo_set)
mydb.close()
#selected option inserted into the table and to skill_set 
#based on the skill set filter the todo list from the search table

