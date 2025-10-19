# train_model.py
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

DB_NAME = "nac_database.db"
TABLE_NAME = "traffic_logs"

print("Starting model training from database...")

# 1. Load Data from SQLite Database
try:
    conn = sqlite3.connect(DB_NAME)
    # Use pandas to read the entire table into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
except Exception as e:
    print(f"Error connecting to database or reading table: {e}")
    print("Please ensure you have run 'database_setup.py' first.")
    exit()

# The rest of the script is largely the same
# 2. Preprocess Data
ip_encoder = LabelEncoder()
proto_encoder = LabelEncoder()

# Combine all IPs to ensure the encoder learns them all
all_ips = pd.concat([df['source_ip'], df['dest_ip']]).unique()
ip_encoder.fit(all_ips)

df['source_ip_encoded'] = ip_encoder.transform(df['source_ip'])
df['dest_ip_encoded'] = ip_encoder.transform(df['dest_ip'])
df['protocol_encoded'] = proto_encoder.fit_transform(df['protocol'])

# 3. Define Features (X) and Target (y)
features = ['source_ip_encoded', 'dest_ip_encoded', 'source_port', 'dest_port', 'protocol_encoded', 'packet_count']
target = 'decision' # Changed from 'label' to 'decision'

X = df[features]
y = df[target]

# 4. Split and Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model training completed.")

# 6. Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 7. Save
joblib.dump(model, 'nac_model.joblib')
joblib.dump(ip_encoder, 'ip_encoder.joblib')
joblib.dump(proto_encoder, 'proto_encoder.joblib')
print("Model and encoders saved successfully.")