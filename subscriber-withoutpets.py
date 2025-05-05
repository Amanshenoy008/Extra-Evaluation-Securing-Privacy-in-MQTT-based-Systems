import paho.mqtt.client as mqtt
import json

# MQTT Secure Broker Config
BROKER = "localhost"
PORT = 1883
TOPIC = "disaster/alerts"

def on_connect(client, userdata, flags, rc):
    print(f"[INFO] Connected with result code {rc}")
    client.subscribe(TOPIC)
    print(f"[INFO] Subscribed to topic: {TOPIC}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"[RECEIVED] {data}")
    except Exception as e:
        print(f"[ERROR] Could not parse message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
