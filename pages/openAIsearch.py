import random
import string
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import mysql.connector
import openai
import streamlit as st
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import getusrname
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
st.header("OpenAI Search")
cursor = mydb.cursor()
add_filequery = ("INSERT INTO fileDetails "
               "( file_name, file_description, user_id , extension_id, file_data, created_date) "
               "VALUES (%s, %s, 1, 8, %s, %s)")

def call_openai_api(chunk):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "PASS IN ANY ARBITRARY SYSTEM VALUE TO GIVE THE AI AN IDENITY"},
            {"role": "user", "content": f"OPTIONAL PREPROMPTING FOLLOWING BY YOUR DATA TO PASS IN: {chunk}."},
        ],
        max_tokens=1750,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0]['message']['content'].strip()

def split_into_chunks(text, tokens=1500):
    words = text.split()
    chunks = [' '.join(words[i:i + tokens]) for i in range(0, len(words), tokens)]
    return chunks


def process_chunks(input_text):
    chunks = split_into_chunks(input_text)
    
    # Processes chunks in parallel
    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(call_openai_api, chunks))

    return responses[0]

search_txt = st.text_input("Please enter detailed description of what you are looking for:")

if st.button('View'):
        #check if there is a valid description
        #otherwise enter description
        fname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        fname = "OpenAI_"+fname
        
        fdata = process_chunks(search_txt)
        st.write("Result:")
        st.write(fdata)
        file_blob = fdata.encode('UTF-8')
        
        current_dateTime= datetime.now()
        file_data = (fname, search_txt, file_blob, current_dateTime)    
        cursor.execute(add_filequery, file_data)
        mydb.commit()
        cursor.close()
        mydb.close()
