import streamlit as st
import mysql.connector
import pandas as pd
from splinter import Browser

from sqlalchemy import create_engine, text

import openai
from concurrent.futures import ThreadPoolExecutor

import string
import random

from datetime import datetime

#from nav_bar import sidebar

#sidebar()

#writing the output to a file is not working 
#look into it

#openai.api_key = "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"
#openai.api_key = "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"
openai.api_key = "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"

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

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
        
        fdata = process_chunks(search_txt)
        st.write(fdata)
        file_blob = fdata.encode('UTF-8')
        
        current_dateTime= datetime.now()
        file_data = (fname, search_txt, file_blob, current_dateTime)    
        cursor.execute(add_filequery, file_data)
        mydb.commit()
        cursor.close()
        mydb.close()
