import streamlit as st
import mysql.connector
import pandas as pd
#from nav_bar import sidebar

#sidebar()

query_params = st.experimental_get_query_params()
file_id = query_params.get("key1")

st.header("View Log")
#fetch log details from database

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

df1 = pd.read_sql("SELECT * FROM fileDetails WHERE file_id = %d " % (int(file_id[0])), mydb)

mydb.close()
#st.write("Search Description: "+str(df1["file_description"][0]))
st.text_input("Search Description: ", value=str(df1["file_description"][0]), disabled=True)
st.write("Searched date : "+str(df1["created_date"][0]))
st.write("OpenAI response:")
fdata = df1["file_data"][0].decode('UTF-8')
st.write(fdata)

