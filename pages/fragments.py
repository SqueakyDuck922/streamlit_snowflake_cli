import streamlit as st
import pandas as pd
from datetime import datetime


st.text("Here is a basic example of defining and calling a fragment function")

@st.fragment
def fragment_function():
    if st.button("Hi!"):
        st.write("Hi back!")

fragment_function()



st.text("If you want the main body of your fragment to appear in the sidebar or another container, call your fragment function inside a context manager.")

with st.sidebar:
    fragment_function()



st.title("Fragment execution flow")


st.text(" If you flip the toggle button in your running app, the first fragment (toggle_and_text()) will rerun, redrawing the toggle and text area while leaving everything else unchanged. If you click the checkbox, the second fragment (filter_and_file()) will rerun and consequently redraw the checkbox and file uploader. Everything else remains unchanged. Finally, if you click the update button, the full script will rerun, and Streamlit will redraw everything.")

@st.fragment()
def toggle_and_text():
    cols = st.columns(2)
    cols[0].toggle("Toggle")
    cols[1].text_area("Enter text")

@st.fragment()
def filter_and_file():
    cols = st.columns(2)
    cols[0].checkbox("Filter")
    cols[1].file_uploader("Upload image")

toggle_and_text()
cols = st.columns(2)
cols[0].selectbox("Select", [1,2,3], None)
cols[1].button("Update")
filter_and_file()


def get_latest_updates():
    df = pd.DataFrame({
    "time": [datetime.now()],
    "value": [42]  # constant value
    })
    return df



st.title("Automate fragment reruns")

@st.fragment(run_every="10s")
def auto_function():
    # This will update every 10 seconds!
    st.text("this fragment will update every 10 seconds")
    df = get_latest_updates()
    st.line_chart(df)
    st.text(str(df.loc[0, "time"]))

auto_function()