# combine the MQTT and RF receive codes 
import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish 
import picamera 
import argparse 
import signal 
import sys 
import time 
import logging 

### camera 
camera = picamera.PiCamera() 
camera.vflip=True 
#
def post_image(): 
   print('Taking photo') 
   camera.capture('image.jpg') 
   file_name = 'image_' + str(datetime.now()) + '.jpg' 
   camera.capture(file_name)  # time-stamped image 
   with open('image.jpg', "rb") as imageFile: 
       myFile = imageFile.read() 
       data = bytearray(myFile) 
   client.publish('dev/camera', data, mqttQos, mqttRetained)  # 
   client.publish('dev/test', 'Capture!') 
   print(file_name + 'image published') 

### MQTT 
broker = '192.168.0.100' 
topic ='dev/test' 
mqttQos = 0 
mqttRetained = False 
#
def on_connect(client, userdata, flags, rc): 
   print("Connected with result code "+str(rc)) 
   client.subscribe(topic) 
# The callback for when a PUBLISH message is received from the server.
# 
def on_message(client, userdata, msg): 
   payload = str(msg.payload.decode('ascii'))  # decode the binary string 
   print(msg.topic + " " + payload) 
   process_trigger(payload) 
#
def process_trigger(payload): 
   if payload == 'ON': 
       print('ON triggered') 
       post_image() 
#
client = mqtt.Client() 
client.on_connect = on_connect    # call these on connect and on message 
client.on_message = on_message 
client.username_pw_set(username='user',password='pass')  # need this 
client.connect(broker) 
client.loop_forever() #  don't get past this 
#client.loop_start()   #  run in background and free up main thread 