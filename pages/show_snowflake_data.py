import streamlit as st

st.title("here we display data from a snowflake database")


# This works when deployed to Snowflake:

conn = st.connection("snowflake")

# df = conn.query("SELECT COL1,COL2 FROM DEV_STREAMLIT_DEMO.SCHEMA1.DAFT_TABLE;", ttl="10m")
df = conn.query("SELECT COL1,COL2 FROM DAFT_TABLE;", ttl="10m") # Works also without qualifying the the database and schema , think because when deploy the BIC_marketplace connection is passed which includes these

for row in df.itertuples():
    st.write(f"{row.COL1} has a :{row.COL2}:")



# session = conn.session()

# session.sql("SELECT 1").collect()