# app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- Globals for Database and Model ---
DB_NAME = "nac_database.db"
TABLE_NAME = "traffic_logs"
model = joblib.load('nac_model.joblib')
ip_encoder = joblib.load('ip_encoder.joblib')
proto_encoder = joblib.load('proto_encoder.joblib')
label_encoder = joblib.load('label_encoder.joblib')


# --- MODIFIED: Function now ONLY clears the database ---
def initialize_database():
    """Wipes the existing logs so the session starts fresh."""
    print("Initializing database for a new session...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Delete all existing records from the table
    cursor.execute(f"DELETE FROM {TABLE_NAME};")
    # Optional: Reset the autoincrement counter
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{TABLE_NAME}';")
    print(f"Cleared all previous records from '{TABLE_NAME}'. Database is now empty.")

    conn.commit()
    conn.close()
    print("Database initialization complete.")


def log_to_database(data, decision):
    """Saves the traffic data and the model's decision to the database."""
    conn = sqlite3.connect(DB_NAME)
    query = f"""
        INSERT INTO {TABLE_NAME} (timestamp, source_ip, dest_ip, source_port, dest_port, protocol, packet_count, decision)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    timestamp = datetime.now().isoformat()
    
    conn.execute(query, (
        timestamp, data['source_ip'], data['dest_ip'], data['source_port'],
        data['dest_port'], data['protocol'], data['packet_count'], decision
    ))
    
    conn.commit()
    conn.close()
    print(f"Logged new entry to database with decision: {decision}")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    df = pd.DataFrame([data])
    
    try:
        df['source_ip_encoded'] = ip_encoder.transform(df['source_ip'])
        df['dest_ip_encoded'] = ip_encoder.transform(df['dest_ip'])
        df['protocol_encoded'] = proto_encoder.transform(df['protocol'])
    except Exception:
        decision = 'denied'
        log_to_database(data, decision)
        return jsonify({'prediction': decision, 'reason': 'Unseen IP or Protocol'})

    features = ['source_ip_encoded', 'dest_ip_encoded', 'source_port', 'dest_port', 'protocol_encoded', 'packet_count']
    prediction_encoded = model.predict(df[features])[0]
    
    # Decode the prediction back to 'allowed' or 'denied'
    prediction = label_encoder.inverse_transform([prediction_encoded])[0]
    
    log_to_database(data, prediction)
    
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    initialize_database()
    print("Model and encoders loaded. Starting Flask server.")
    app.run(host='0.0.0.0', port=5000, debug=False)
