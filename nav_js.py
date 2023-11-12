import streamlit as st
from streamlit.components.v1 import html

def setusrname(val):
    global username
    username = val

def getusrname():
    try:
        return username 
    except Exception as e:
        return ""
    
def headerstyle():
    st.markdown("""
    <style>
        iFrame{
        margin-bottom : -140px;           
        }          
    </style>""", unsafe_allow_html=True)

def navbar_loggedOut(page):

    js_code1 ="""
    <style>
    body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    }

    .topnav {
    overflow: hidden;
    background-color: #333;
    }

    .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 50px;
    text-decoration: none;
    font-size: 18px;
    }

    .topnav a:hover {
    background-color: #ddd;
    color: black;
    }

    .topnav a.active {
    background-color: #04AA6D;
    color: white;
    }

    h2 {
    margin-top: -120px;
    }

    </style>
    </head>
    """

    js_code2 =f"""
    <div class="topnav">
    <a id="home" href="/home" target="_target">Home</a>
    <a id="about" href="/aboutus" target="_target">About Us</a>
    <a id="search" href="/search" target="_target">Search</a>
    <a id="login" href="/login" target="_target">Log In</a>
    </div>
    <script>
    var curr_page = "{page}";
    """

    js_code3 ="""
    var home_ele = document.getElementById("home");
    var about_ele = document.getElementById("about");
    var search_ele = document.getElementById("search");
    var login_ele = document.getElementById("login");

    switch(curr_page){
        case "home":
            home_ele.classList.add("active");
            break;

        case "about":
            about_ele.classList.add("active");
            break;

        case "search":
            search_ele.classList.add("active");
            break;

        case "login":
            login_ele.classList.add("active");
            break;

    }

    </script>
    """

    html(js_code1+js_code2+js_code3)


def navbar_loggedIn(page):

    js_code1 ="""
    <style>
    body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    }

    .topnav {
    overflow: hidden;
    background-color: #333;
    }

    .topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 50px;
    text-decoration: none;
    font-size: 18px;
    }

    .topnav a:hover {
    background-color: #ddd;
    color: black;
    }

    .topnav a.active {
    background-color: #04AA6D;
    color: white;
    }

    h2 {
    margin-top: -120px;
    }

    </style>
    </head>
    """

    js_code2 =f"""
    <div class="topnav">
    <a id="home" href="/home" target="_target">Home</a>
    <a id="about" href="/aboutus" target="_target">About Us</a>
    <a id="search" href="/search" target="_target">Search</a>
    <a id="searchlogs" href="/search_logs" target="_target">Search Logs</a>
    <a id="todosearch" href="/todo_search" target="_target">Todo</a>
    <a id="profile" href="/profile" target="_target">Profile</a>
    <a id="logout" href="/logout" target="_target">Log Out</a>
    </div>
    <script>
    var curr_page = "{page}";
    """

    js_code3 ="""
    var home_ele = document.getElementById("home");
    var about_ele = document.getElementById("about");
    var search_ele = document.getElementById("search");
    var searchlogs_ele = document.getElementById("searchlogs");
    var todosearch_ele = document.getElementById("todosearch");
    var profile_ele = document.getElementById("profile");
    var logout_ele = document.getElementById("logout");

    switch(curr_page){
        case "home":
            home_ele.classList.add("active");
            break;

        case "about":
            about_ele.classList.add("active");
            break;

        case "search":
            search_ele.classList.add("active");
            break;

        case "searchlogs":
            searchlogs_ele.classList.add("active");
            break
            
        case "todo":
            todosearch_ele.classList.add("active");
            break
            
        case "profile":
            profile_ele.classList.add("active");
            break
        
        case "logout":
            logout_ele.classList.add("active");
            break;

    }

    </script>
    """

    html(js_code1+js_code2+js_code3)
