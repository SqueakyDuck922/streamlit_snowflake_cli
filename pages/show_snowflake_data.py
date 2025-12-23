import streamlit as st

st.title("here we display data from a snowflake database")


# This works both when deployed to Snowflake and running locally (locally requires secrets.toml)

conn = st.connection("snowflake")

df = conn.query("SELECT COL1,COL2 FROM DAFT_TABLE;", ttl="10m") # Works without qualifying the the database and schema. These are contained in secrets.toml / connections.toml

for row in df.itertuples():
   st.write(f"{row.COL1} has a :{row.COL2}:")



# session = conn.session()

# session.sql("SELECT 1").collect()