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
print("Model and encoders loaded.")

def log_to_database(data, decision):
    """Saves the traffic data and the model's decision to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = f"""
        INSERT INTO {TABLE_NAME} (timestamp, source_ip, dest_ip, source_port, dest_port, protocol, packet_count, decision)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    # Get current timestamp
    timestamp = datetime.now().isoformat()
    
    # Execute the query
    cursor.execute(query, (
        timestamp,
        data['source_ip'],
        data['dest_ip'],
        data['source_port'],
        data['dest_port'],
        data['protocol'],
        data['packet_count'],
        decision
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
        # If an IP/protocol is unseen, deny it and log it for future training
        decision = 'denied'
        log_to_database(data, decision)
        return jsonify({'prediction': decision, 'reason': 'Unseen IP or Protocol'})

    features = ['source_ip_encoded', 'dest_ip_encoded', 'source_port', 'dest_port', 'protocol_encoded', 'packet_count']
    prediction = model.predict(df[features])[0]
    
    # Log the request and its outcome to the database
    log_to_database(data, prediction)
    
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) # Turned debug off for cleaner logging