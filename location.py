import paho.mqtt.client as mqtt
from datetime import datetime
import time
import re

# List to store messages
messages = []

# Callback function for connection
def connection(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("Connected OK Returned code=", rc)
        client.subscribe("owntracks/SS/#")
        client.subscribe("collar/logs")
    else:
        print("Connection Unsuccessful, Error message:", rc)

# Callback function for disconnect
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# Function to extract battery information
def extract_battery_info(message):
    word_to_extract = "batt"
    characters_after_word = 4
    pattern = re.compile(r'\b{}\b(.{{0,{}}})'.format(re.escape(word_to_extract), characters_after_word))
    match = pattern.search(message)
    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return None

# Callback function for receiving messages
def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = msg.payload.decode("utf8")
        messages.append(payload)
        
        # Log message with timestamp
        log_message(topic, payload)
        
        # Extract battery info if available
        battery_info = extract_battery_info(payload)
        if battery_info:
            log_battery_info(battery_info)

    except Exception as e:
        print(f"Error decoding message: {e}")

# Function to log messages with timestamps
def log_message(topic, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("cat_collar_logs.txt", "a") as log_file:
        log_file.write(f"{timestamp} - Topic: {topic} - Message: {message}\n")

# Function to log battery information
def log_battery_info(battery_info):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("cat_collar_battery_logs.txt", "a") as battery_log_file:
        battery_log_file.write(f"{timestamp} - Battery Info: {battery_info}\n")

# Setup MQTT client
client = mqtt.Client(userdata={'logs': []})
client.on_connect = connection
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the MQTT broker
client.connect("broker.hivemq.com", 1883)

# Start the MQTT client loop
client.loop_forever()


