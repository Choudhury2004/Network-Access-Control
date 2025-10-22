# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

CSV_FILE = "network_traffic.csv"

print("Starting model training from CSV file...")

# 1. Load Data directly from CSV
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"Error: Training file '{CSV_FILE}' not found.")
    exit()

# The rest of the script remains the same
# 2. Preprocess Data
ip_encoder = LabelEncoder()
proto_encoder = LabelEncoder()
label_encoder = LabelEncoder() # For the 'label' column

# Combine all IPs to ensure the encoder learns them all
all_ips = pd.concat([df['source_ip'], df['dest_ip']]).unique()
ip_encoder.fit(all_ips)

df['source_ip_encoded'] = ip_encoder.transform(df['source_ip'])
df['dest_ip_encoded'] = ip_encoder.transform(df['dest_ip'])
df['protocol_encoded'] = proto_encoder.fit_transform(df['protocol'])
df['label_encoded'] = label_encoder.fit_transform(df['label'])


# 3. Define Features (X) and Target (y)
features = ['source_ip_encoded', 'dest_ip_encoded', 'source_port', 'dest_port', 'protocol_encoded', 'packet_count']
target = 'label_encoded'

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
joblib.dump(label_encoder, 'label_encoder.joblib') # Save the label encoder as well
print("Model and encoders saved successfully.")
