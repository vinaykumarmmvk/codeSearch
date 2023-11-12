import streamlit as st
from streamlit.components.v1 import html

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)

def open_pageself(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_self');
        </script>
    """ % (url)
    html(open_script)