# dashboard.py
import streamlit as st
import pandas as pd
import sqlite3
import time

st.set_page_config(layout="wide", page_title="NAC Dashboard")

DB_NAME = "nac_database.db"
TABLE_NAME = "traffic_logs"

def load_data():
    """Loads data from the SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

st.title("🛡️ Live Network Access Control Dashboard")
st.write("This dashboard connects directly to the database and shows the most recent traffic.")

# --- Main Page Layout ---
placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        st.header("Real-time Traffic Logs")
        st.dataframe(df)

        col1, col2 = st.columns(2)
        with col1:
            st.header("Protocol Distribution")
            st.bar_chart(df['protocol'].value_counts())
        with col2:
            st.header("Access Decisions")
            st.bar_chart(df['decision'].value_counts())
    
    time.sleep(5) # Refresh interval in seconds