import socket
import sys
import base64
import threading
import requests
import os
import codecs
# import paho.mqtt.client as mqtt

import cv2
import numpy as np

import urllib3
import socketserver
import time
from datetime import datetime


# Listen on
HOST = ''
#HOST = '0.0.0.0'
PORT = 9000

CAMERA_READ_TIMEOUT  = 4  # seconds
BACKEND_SEND_TIMEOUT = 1  # seconds


def post_image(image_base_64): 
    print('Sending photo:', datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) 
    # send image
    url = 'http://heimdall-backend:5000/api/live/'
    data = {'image': image_base_64, 'annotate': 'True'}
    
    try:
        requests.post(url, data=data, timeout=BACKEND_SEND_TIMEOUT)
    except requests.exceptions.ReadTimeout as e:
        print("ReadTimeout: Heimdall backend not responding on time!")
    except (urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError) as e:
        print("NewConnectionError: Heimdall backend not responding!")

'''
### MQTT 
#broker = 'mqtt-broker' 
broker = os.environ.get('MQTT_BROKER_IP')
#broker = 'localhost'
topic ='trigger' 
mqttQos = 0
mqttRetained = False 




def post_image(image_base_64): 
    print("============")
    print('Sending photo') 
    (result, mid) = client.publish("camera", image_base_64, mqttQos, mqttRetained)
    print('Result:', result, '- Mid:', mid)


def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    client.subscribe(topic) 
    
# The callback for when a PUBLISH message is received from the server.
# 
def on_message(client, userdata, msg): 
    print("=========")
    payload = str(msg.payload.decode('ascii'))  # decode the binary string 
    print("on_message: " + msg.topic + " " + payload) 

def on_publish(client, obj, mid):
    print("Publish - Mid:", mid)
    print("=========")

def on_log(client, userdata, level, buf):
    print(level, buf)

def on_disconnect(client, userdata, rc):
    print("=========")
    print("Disconnected:", mqtt.connack_string(rc))


client = mqtt.Client(client_id="heimdall-camera")  # protocol=mqtt.MQTTv31

client.on_connect = on_connect    # call these on connect and on message 
client.on_message = on_message
client.on_publish = on_publish 
client.on_disconnect = on_disconnect
#client.on_log = on_log

#client.username_pw_set(username='user',password='pwd')  # need this 

print("Connecting to broker: " + broker)
client.connect(broker, 1883, 60) 
# client.loop_forever()    #  don't get past this 
client.loop_start()    #  run in background and free up main thread

'''


class CameraTCPHandler(socketserver.BaseRequestHandler):

    def read(self):
        image = b''
        while True:
            # Receiving from client
            data = self.request.recv(4096)
            if not data:
                break
            #print("More data: " + str(sys.getsizeof(data)))
            image += data
        
        number_of_bytes = 3
        voltage = int(image[-number_of_bytes:]) / 100.0
        print(" ")
        #print("Voltage RAW:", image[-number_of_bytes:])
        print("Voltage:", voltage)
        #print(image[-30:])
        image = image[:-number_of_bytes].strip()
        #print(image[-30:])
        return image

    def handle(self):
        self.request.settimeout(CAMERA_READ_TIMEOUT)

        try:
            image = self.read()
            image = codecs.decode(image, "hex")
            
            #nparr = np.fromstring(image, np.uint8)
            #image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # send image
            image_base_64 = base64.b64encode(image)
            post_image(image_base_64)
        except socket.timeout as te:
            print("Timeout Exception: Looks like the camera closed the connection")




class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


print("Socket listening on {}:{}".format(HOST, PORT))
server = ThreadedTCPServer((HOST, PORT), CameraTCPHandler)
server.serve_forever()
