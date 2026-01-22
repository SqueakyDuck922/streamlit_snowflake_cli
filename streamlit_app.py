import streamlit as st
import common.functions as fc

from common.hello import say_hello

st.title(f"Example streamlit chicken app. {say_hello()}")



if "snowflake_session" not in st.session_state:
    st.session_state["snowflake_session"] = fc.get_session()

session = st.session_state["snowflake_session"]