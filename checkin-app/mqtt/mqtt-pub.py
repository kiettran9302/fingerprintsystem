import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_SERVER_PORT = 1883
MQTT_PATH = "/dev/checkin"
import time
import json

client = mqtt.Client()
client.connect(MQTT_SERVER, MQTT_SERVER_PORT)

count = 2
while True:
    payload = {
            'id': count
    }
    client.publish(topic=MQTT_PATH, payload=json.dumps(payload))
    time.sleep(1)