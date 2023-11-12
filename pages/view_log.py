import streamlit as st
import mysql.connector
import pandas as pd
from nav_js import navbar_loggedOut
from nav_js import navbar_loggedIn
import time
from nav_js import headerstyle

st.set_page_config(initial_sidebar_state="collapsed",
    layout="wide")

time.sleep(1)
navbar_loggedIn("searchlogs")

headerstyle()

query_params = st.experimental_get_query_params()
searchId = query_params.get("key1")

st.header("View Log")
#fetch log details from database

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "1234",
	database = "codesearch"
)

#query = "Select * from searchData where search_id ="+str(searchId)
df = pd.read_sql("SELECT * FROM searchData WHERE search_id = %d " % (int(searchId[0])), mydb)
#df = pd.read_sql(query, mydb)

st.subheader("Search Log id "+searchId[0])
st.write("**searched for**      : "+df["searched_for"][0])

searchedFor = df["searched_for"][0]
ext_id = df["extension_id"][0]

st.write("Result Exists: "+str(df["result_exists"][0]))
st.write("Extension Id : "+str(df["extension_id"][0]))
st.write("Search Date : "+str(df["search_date"][0]))

dfCount = pd.read_sql("select * from searchData where searched_for like '%s' and extension_id =%s " % (searchedFor, int(ext_id)), mydb)
mydb.close()
st.write("Count/frequency : "+str(dfCount.size))
download_data = "Searched for: "+searchedFor+"\n Extension Id:"+str(ext_id)+"\n Search Date:"+str(df["search_date"][0])+"\n Result exists: "+str(df["result_exists"][0])+"\n Frequency: "+str(dfCount.size)
st.download_button('Download', download_data, file_name=searchedFor+".txt")
#st.text_input(":red[Searched for]", disabled=True,value="test")
