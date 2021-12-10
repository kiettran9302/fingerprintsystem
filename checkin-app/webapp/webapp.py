from flask import Flask, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
import paho.mqtt.client as mqtt
import json
import sys
sys.path.insert(0, '../db')
import db_access

'''===================DB================='''
db_inst = db_access.DB('../db/checkindb.db')

'''===================WEB_HANDLER================='''
app = Flask(__name__)
app.secret_key = 'checkinapponlyforteacherauthorization'

#index page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('mainboard'))
    else:
        return redirect(url_for('login'))

#login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        #get username, password
        input_usrname = request.form['usrname']
        input_pswd = request.form['pswd']
        #check if account exist in db
        account_result = db_inst.retrieve_account(input_usrname, input_pswd)
        if (len(account_result) > 0):
            session['user_id'] = input_usrname
            return redirect(url_for('mainboard'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

#logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

#mainboard page
@app.route('/mainboard', methods=['POST', 'GET'])
def mainboard():
    if 'user_id' in session:
        return render_template('mainboard.html')
    else:
        return redirect(url_for('login'))


'''===================MQTT_HANDLER================='''
MQTT_SERVER = "localhost"
MQTT_SERVER_PORT = 1883
MQTT_SUB_TOPICS = [
    '/dev/checkin',
]
MQTT_PUB_TOPICS = [
    '/webserver/checkin/db',
    '/webserver/checkin/student'
]

mqtt_client = mqtt.Client()

def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(mqtt_client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    payload = json.loads(msg.payload)
    if (msg.topic == MQTT_SUB_TOPICS[0]):
        #update checkin status in db
        student = db_inst.retrieve_student(payload['id'])
        db_inst.update_checkin_status('YES', student[0]['id'], '2021-11-19')
        #query database and pub checkin_status to teacher
        checkin_result = db_inst.retrieve_checkin_status_join_student()
        mqtt_client.publish(topic=MQTT_PUB_TOPICS[0], payload=json.dumps(checkin_result))
        #query db get student name and send back to hardware
        mqtt_client.publish(topic=MQTT_PUB_TOPICS[1], payload=json.dumps(student))
    
def mqtt_run():
    mqtt_client.connect(MQTT_SERVER, MQTT_SERVER_PORT)

    for topic in MQTT_SUB_TOPICS:
        mqtt_client.subscribe(topic)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()


if __name__ == "__main__":
    mqtt_run()
    app.run(host='172.16.2.129', port='80')
