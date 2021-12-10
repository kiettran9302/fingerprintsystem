import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_SERVER_PORT = 1883
MQTT_PATH = "/myroot"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
#client.username_pw_set("pi", "raspberry")
client.connect(MQTT_SERVER, MQTT_SERVER_PORT) 
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()