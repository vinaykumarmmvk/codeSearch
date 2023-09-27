import streamlit as st
import mysql.connector
import pandas as pd
#from nav_bar import sidebar

#sidebar()
#show all the information of the log and edit button to add code to it, if user is specalized in it.


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

st.write("result exists: "+str(df["result_exists"][0]))
st.write("extension_id :"+str(df["extension_id"][0]))
st.write("search_date :"+str(df["search_date"][0]))

mydb.close()

#dfCount = pd.read_sql("select * from searchData where searched_for like '%s' "% (searchedFor) %" and extension_id =%s " % (int(ext_id)), mydb)
mysql_statement = """SELECT * FROM searchData where searched_for like '%s' and extension_id = %d """
dfCount = pd.read_sql(mysql_statement, con=mydb, params=(searchedFor, int(ext_id)))
st.write("Count/frequency ")
st.write(dfCount)
#st.text_input(":red[Searched for]", disabled=True,value="test")
