import streamlit as st
import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['abc123', 'def456']).generate()
st.write(hashed_passwords)