import paho.mqtt.client as mqtt
import time
import json
import random



# victim message contents
messages = [
    {"user_id": "victim_01", "location": "37.7749,-122.4194", "message": "Stuck on rooftop!","device_id": "Samsung",},
    {"user_id": "victim_02", "location": "37.8044,-122.2711", "message": "Need medical help!","device_id": "Iphone",},
    {"user_id": "victim_03", "location": "37.7600,-122.4477", "message": "Water level rising fast!","device_id": "Micromax",},
]

BROKER = "localhost"
PORT = 1883
TOPIC = "disaster/alerts"

def on_connect(client, userdata, flags, rc):
    print(f"[INFO] Connected with result code {rc}")

client = mqtt.Client()        # create client to send message
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

try:                 # the publisher continues sending messages 
    while True:
        msg = random.choice(messages)
        payload = json.dumps(msg)
        result = client.publish(TOPIC, payload)
        if result[0] == 0:
            print(f"[PUBLISH] Sent: {payload}")
        else:
            print("[ERROR] Failed to send message")
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n[INFO] Publisher stopped.")
    client.loop_stop()
