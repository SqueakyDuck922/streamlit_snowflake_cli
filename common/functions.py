import streamlit as st


# +---------------------+
# |    AUTHENTICATION   |
# +---------------------+

def get_session():
    try:
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
        if session:
            return session
        # If session is None, raise to trigger fallback
        raise RuntimeError("No active Snowflake session found.")
    except Exception:
        # Local fallback
        from snowflake.snowpark import Session
        from dotenv import load_dotenv
        import os

        load_dotenv()
        # connection_params = {
        #     "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        #     "user": os.getenv("SNOWFLAKE_USER"),
        #     "authenticator": "externalbrowser",
        #     "role": os.getenv("SNOWFLAKE_ROLE"),
        #     "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        #     "database": os.getenv("SNOWFLAKE_DATABASE"),
        #     "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        # }

        connection_params = {
            "account": st.secrets["connections"]["snowflake"]["account"],
            "user": st.secrets["connections"]["snowflake"]["user"],
            "password": st.secrets["connections"]["snowflake"]["password"],
            "warehouse": st.secrets["connections"]["snowflake"]["warehouse"],
            "database": st.secrets["connections"]["snowflake"]["database"],
            "schema":  st.secrets["connections"]["snowflake"]["schema"]
        }

        session = Session.builder.configs(connection_params).create()
        Session._default_session = session
        return session