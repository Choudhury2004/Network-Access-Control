# dashboard.py
import streamlit as st
import pandas as pd
import sqlite3
import time

st.set_page_config(layout="wide", page_title="NAC Dashboard")

# --- 1. AUTHENTICATION LOGIC ---

def check_login(username, password):
    """Checks if the username and password are correct."""
    return username == "admin" and password == "admin1234"

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 2. LOGIN PAGE UI ---

if not st.session_state['logged_in']:
    st.title("🛡️ NAC Dashboard Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if check_login(username, password):
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid username or password")

# --- 3. MAIN DASHBOARD UI ---

else:
    DB_NAME = "nac_database.db"
    TABLE_NAME = "traffic_logs"

    @st.cache_data(ttl=5)
    def load_data():
        """Loads all data from the SQLite database."""
        try:
            conn = sqlite3.connect(DB_NAME)
            df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC", conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error connecting to database: {e}")
            return pd.DataFrame()

    st.title("🛡️ Live Network Access Control Dashboard")
    df = load_data()

    st.header("Live Traffic Filter")
    st.text_input(
        "Filter by Source IP:", 
        placeholder="e.g., 192.168.1.10", 
        key='source_ip_filter'
    )

    df_display = df.copy()

    if st.session_state.source_ip_filter.strip():
        df_display = df_display[df_display['source_ip'] == st.session_state.source_ip_filter.strip()]

    # --- NEW: Function to apply color styling ---
    def color_decision(val):
        """
        Takes a string and returns a color style.
        'denied' will be red, 'allowed' will be green.
        """
        color = 'red' if val == 'denied' else 'green' if val == 'allowed' else 'white'
        return f'color: {color}'

    st.header("Real-time Traffic Logs")
    
    # Apply the styling function to the 'decision' column
    styled_df = df_display.style.applymap(color_decision, subset=['decision'])
    
    # Display the styled DataFrame
    st.dataframe(styled_df)


    st.header("Filtered Analytics")

    if not df_display.empty:
        col1_charts, col2_charts = st.columns(2)
        with col1_charts:
            st.subheader("Protocol Distribution")
            st.bar_chart(df_display['protocol'].value_counts())
        with col2_charts:
            st.subheader("Access Decisions")
            st.bar_chart(df_display['decision'].value_counts())
    else:
        st.warning("No data found for the selected filter combination.")

    st.caption("Page automatically refreshes with new data every 5 seconds.")

    time.sleep(5)
    st.rerun()
