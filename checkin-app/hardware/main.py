import ssd1306
import as608
import time
import json
import datetime
#MQTT connection
import paho.mqtt.client as mqtt

with open('./../common.json') as f:
    common = json.load(f)

MQTT_SERVER = common["MQTT_SERVER"]["ADDR"]
MQTT_SERVER_PORT = common["MQTT_SERVER"]["PORT"]
MQTT_SUB_TOPICS = [
    '/webserver/checkin/student'
]
MQTT_PUB_TOPICS = [
    '/dev/checkin',
]

is_granted = 0
student_name = ""
mqtt_client = mqtt.Client()

def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(mqtt_client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))
    #receive name
	if (msg.topic == MQTT_SUB_TOPICS[0]):
		recv_payload = json.loads(msg.payload)
		global student_name
		student_name = str(recv_payload[0]['student_lname'] + ' ' + recv_payload[0]['student_fname'])
		global is_granted
		is_granted = 1
       
def mqtt_run():
    mqtt_client.connect(MQTT_SERVER, MQTT_SERVER_PORT)

    for topic in MQTT_SUB_TOPICS:
        mqtt_client.subscribe(topic)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()
    
    
#init
as608_inst = as608.AS608()
ssd1306_inst = ssd1306.SSD1306()
mqtt_run()

#while run
while True:
	ssd1306_inst.draw.rectangle((0,0,ssd1306_inst.width,ssd1306_inst.height), outline=0, fill=0)
	now = datetime.datetime.now()
	ssd1306_inst.draw.text((23,0), str(now.strftime('%Y-%m-%d %H:%M:%S')),font =ssd1306_inst.font, fill = 255)
	if as608_inst.get_fingerprint():
		payload = {
            'id': as608_inst.finger.finger_id
        	}
		mqtt_client.publish(topic=MQTT_PUB_TOPICS[0], payload=json.dumps(payload))

	print(is_granted)
	if is_granted:
	    print(student_name)
	    ssd1306_inst.draw.text((0, 18), student_name, font=ssd1306_inst.font, fill=255)
	    student_name = ""
	    is_granted = 0
	else:
	    ssd1306_inst.draw.text((0,18),"Please wait...", font = ssd1306_inst.font, fill = 255)
    
	# Display image.
	ssd1306_inst.disp.image(ssd1306_inst.image)
	ssd1306_inst.disp.display()
	time.sleep(.1)
