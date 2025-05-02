import paho.mqtt.client as mqtt
import json
import hashlib
from cryptography.fernet import Fernet

# MQTT Secure Broker Config
BROKER = "localhost"
PORT = 8883
BASE_TOPIC = "disaster/alerts"

# PET: Obfuscate topic (must match publisher)
def obfuscate_topic(topic):
    return hashlib.sha256(topic.encode()).hexdigest()

TOPIC = obfuscate_topic(BASE_TOPIC)

# Paste the encryption key printed by publisher here
key = b'cSiH_xCt6sWto35WALxo696uZlG0dXEijl53o9bvYU4='
cipher = Fernet(key)

# MQTT connect callback
def on_connect(client, userdata, flags, rc):
    print(f"[INFO] Connected with result code {rc}")
    client.subscribe(TOPIC)
    print(f"[INFO] Subscribed to topic: {TOPIC}")

# MQTT message callback
def on_message(client, userdata, msg):
    try:
        decrypted = cipher.decrypt(msg.payload)
        data = json.loads(decrypted.decode())
        print(f"[RECEIVED] {data}")
    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}")

# Setup client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.tls_set()
client.connect(BROKER, 1883, 60)
client.loop_forever()
