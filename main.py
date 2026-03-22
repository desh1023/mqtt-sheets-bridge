import paho.mqtt.client as mqtt
import requests
import json

# Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "sudesh/tunnel/sensor_data"
# Replace with the URL you got after deploying your Apps Script
GOOGLE_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxWup_h-2-fB_kkRmqShHUbYs2maUTrLKlzq8iqn1mnNppb64cTvmgreAQMdr1mUexEyg/exec"

def on_message(client, userdata, msg):
    print(f"Received data on {msg.topic}")
    
    # Prepare the payload for Google Sheets
    payload = {
        "topic": msg.topic,
        "value": msg.payload.decode("utf-8")
    }
    
    try:
        # Forward the data to Google Apps Script
        response = requests.post(GOOGLE_WEB_APP_URL, json=payload, timeout=10)
        print(f"Google Sheets Response: {response.text}")
    except Exception as e:
        print(f"Failed to send to Google: {e}")

# Setup MQTT Client
client = mqtt.Client()
client.on_message = on_message

print("Connecting to broker...")
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"Listening for ESP32 data on {MQTT_TOPIC}...")
# client.loop_forever()
