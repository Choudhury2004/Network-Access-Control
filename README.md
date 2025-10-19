# Network-Access-Control
The Network Access Control (NAC) system is a cybersecurity project that automatically detects, authenticates, and manages devices attempting to access a secured network. It ensures that only trusted and compliant devices are allowed to connect, preventing unauthorized access and network threats.

This project integrates Machine Learning, Backend Automation, and an intuitive User Interface to simulate enterprise-level access control mechanisms.

🚀 Features:
1. Automatic Device Detection – Monitors network traffic and identifies new devices attempting to connect.
2. ML-Based Classification – Uses a trained model to classify devices as trusted, guest, or unauthorized based on features such as MAC address patterns, IP behavior, and traffic volume.
3. Dynamic Database Update – Backend automatically updates the database in real-time when a new device connects.
4. Admin Dashboard (UI) – Displays live device status, connection logs, and access permissions.
5. Secure Access Policies – Enforces customizable access rules for different device categories.

🧠 Tech Stack:
1. Programming Language: Python
2. Machine Learning: Scikit-learn
3. Database: MySQL / SQLite
4. Backend: Flask / FastAPI
5. Networking Tools: scapy

Network-Access-Control/
│
├── backend/
│   ├── instance/
│   │   ├── database.db              # Local SQLite database for backend
│   │   └── device_classifier.pkl    # Trained ML model for classifying devices
│   │
│   └── app.py                       # Main Flask backend server
│
├── instance/
│   └── database.db                  # Global database for NAC operations
│
├── ml_model/
│   └── train_model.py               # Script to train ML model for device behavior analysis
│
├── network_monitor/
│   └── monitor.py                   # Monitors network for new or unknown devices
│
├── venv/                            # Virtual environment for project dependencies
│
├── dashboard.py                     # Flask-based admin dashboard for visual monitoring
│
├── database_setup.py                # Initializes and configures NAC database
│
├── ip_encoder.joblib                # Encoded IP feature mappings for ML preprocessing
├── nac_database.db                  # Main database file storing device details and logs
├── nac_model.joblib                 # Serialized trained ML model for device classification
├── proto_encoder.joblib             # Encoded network protocol mappings
│
├── network_traffic.csv              # Dataset containing captured network traffic details
│
└── README.md                        # Project documentation
