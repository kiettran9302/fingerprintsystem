#!/bin/bash
service mosquitto start
cd /home/pi/Desktop/checkin-app
cd hardware
python3 main.py &
cd ..
cd webapp
python3 webapp.py &