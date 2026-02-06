import streamlit as st


if "var1" in st.session_state:
    st.write(st.session_state["var1"])
else:
    st.write("var1 not in session state")


if "var2" in st.session_state:
    st.write(st.session_state["var2"])
else:
    st.write("var2 not in session state")


with st.form("my_form"):
    submitted = st.form_submit_button("Submit")

    st.write("look this runs even before submit clicked")
    st.session_state["var2"] = "two"

if submitted:
    st.session_state["var1"] = "one"
    # st.rerun()