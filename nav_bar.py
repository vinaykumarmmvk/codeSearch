import streamlit as st
from streamlit_option_menu import option_menu

def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title= "Algorithm code search",
            options=["Search","Login","About Us","Raise request","Todo","Search Request"],
            icons=["search","box-arrow-in-right","file-person","search","box-arrow-in-right","file-person"],
            menu_icon="list-columns-reverse",
            default_index=0,
        )