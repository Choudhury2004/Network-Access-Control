# monitor.py
import requests
import time
import random

# The URL of our Flask API
API_URL = "http://172.22.20.57:5000/predict"

# Sample data to simulate network traffic
sample_ips = ["192.168.1.10", "10.0.5.80", "172.16.31.5", "192.168.1.25"]
sample_protocols = ["TCP", "UDP"]

def generate_traffic_data():
    """Generates a single instance of mock network traffic."""
    traffic = {
        "source_ip": random.choice(sample_ips),
        "dest_ip": random.choice(sample_ips),
        "source_port": random.randint(1024, 65535),
        "dest_port": random.choice([22, 80, 443, 3389, 4444]),
        "protocol": random.choice(sample_protocols),
        "packet_count": random.randint(10, 5000)
    }
    # Ensure source and dest IPs are not the same
    while traffic['source_ip'] == traffic['dest_ip']:
        traffic['dest_ip'] = random.choice(sample_ips)
    return traffic

if __name__ == "__main__":
    print("Starting network monitor simulation...")
    while True:
        # Generate a new traffic event
        traffic_data = generate_traffic_data()
        
        print(f"Monitoring: New connection attempt -> {traffic_data}")

        try:
            # Send data to the Flask app for a prediction
            response = requests.post(API_URL, json=traffic_data)
            response.raise_for_status() # Raise an exception for bad status codes
            
            result = response.json()
            print(f"Decision from NAC: {result['prediction'].upper()}\n")

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to the prediction service: {e}\n")
        
        # Wait for a few seconds before generating the next event
        time.sleep(3)
