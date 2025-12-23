import streamlit as st
from common.hello import say_hello

st.title(f"Example streamlit chicken app. {say_hello()}")



st.write("chicken licken")



st.text_input("what is chicken called?")