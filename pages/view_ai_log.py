import streamlit as st
import mysql.connector
import pandas as pd
#from nav_bar import sidebar

#sidebar()

query_params = st.experimental_get_query_params()
openAI_Id = query_params.get("key1")

st.header("View Log")
#fetch log details from database

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

df = pd.read_sql("SELECT * FROM openAI WHERE openAI_id = %d " % (int(openAI_Id[0])), mydb)

st.subheader("Search Log id "+openAI_Id[0])
st.write("**searched for**      : "+df["search_description"][0])

file_id = df["file_id"][0]



df1 = pd.read_sql("SELECT * FROM fileDetails WHERE file_id = %d " % (int(file_id)), mydb)

mydb.close()

fpath = "openai/"+str(df1["file_name"][0])+".txt"
st.write("Searched date : "+str(df1["created_date"][0]))

with st.expander("Result",True):
   f = open(fpath, 'r') 
   s = f.read()
   st.code(s, language='c')
