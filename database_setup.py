# database_setup.py
import sqlite3
import pandas as pd

DB_NAME = "nac_database.db"
TABLE_NAME = "traffic_logs"
CSV_FILE = "network_traffic.csv"

# Read the initial data
try:
    df = pd.read_csv(CSV_FILE)
    # Rename 'label' to 'decision' to be more generic
    df.rename(columns={'label': 'decision'}, inplace=True) 
except FileNotFoundError:
    print(f"Error: {CSV_FILE} not found. Please create it with initial training data.")
    exit()

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print(f"Creating table '{TABLE_NAME}' in database '{DB_NAME}'...")

# Create the table with an auto-incrementing ID
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        source_ip TEXT NOT NULL,
        dest_ip TEXT NOT NULL,
        source_port INTEGER NOT NULL,
        dest_port INTEGER NOT NULL,
        protocol TEXT NOT NULL,
        packet_count INTEGER NOT NULL,
        decision TEXT NOT NULL
    )
''')

# Write the data from the DataFrame to the SQL table
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("Database setup complete. Initial data has been loaded.")