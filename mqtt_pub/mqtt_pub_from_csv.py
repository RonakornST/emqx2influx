import paho.mqtt.client as mqtt
import csv
import json
import time
import sys

# EMQX broker settings
#MQTT_BROKER = "localhost"  # or use the IP address if running remotely

MQTT_BROKER = "emqx" # Python script runs inside a Docker container (Docker Compose will automatically resolve service names via its internal network.)
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/environment"
CSV_FILE = "cucumber_data.csv"

# Fix the callback signature for VERSION2
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    if rc == 0:
        print("Successfully connected to MQTT broker")
    else:
        print(f"Failed to connect with code {rc}")

# Setup MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # Use VERSION2 to avoid deprecation warning
client.on_connect = on_connect

# Try to connect with retry
max_retries = 20
retry_count = 0
connected = False

while retry_count < max_retries and not connected:
    try:
        print(f"Attempting to connect to {MQTT_BROKER}:{MQTT_PORT} (attempt {retry_count+1})")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(2)  # Wait for connection to establish
        connected = True
        print("Connection established")
    except Exception as e:
        print(f"Connection failed: {e}")
        retry_count += 1
        time.sleep(5)  # Wait before retrying

if not connected:
    print("Failed to connect after multiple attempts. Exiting.")
    sys.exit(1)

# Read CSV and publish
with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        payload = json.dumps(row)
        result = client.publish(MQTT_TOPIC, payload)
        print(f"Published: {payload} (Success: {result.rc == 0})")
        time.sleep(1)  # Simulate delay between messages

client.disconnect()
