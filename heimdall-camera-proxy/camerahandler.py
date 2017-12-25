import socket
import sys
import base64
import threading
import requests
import os
import codecs
import paho.mqtt.client as mqtt

import cv2
import numpy as np

import socketserver



import multiprocessing.pool
import functools

def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator







# Listen on
HOST = ''
#HOST = '0.0.0.0'
PORT = 9000

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
    print(result, ' - ', mid)


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
    print("=========")
    print("Publish - Mid:", mid)

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



import time


class CameraTCPHandler(socketserver.BaseRequestHandler):

    @timeout(2)  # if execution takes longer than X seconds, raise a TimeoutError
    def handle(self):

        image = b''
        print('Receiving data..')
        while True:
            # Receiving from client
            data = self.request.recv(4096)
            if not data:
                break
            #print("More data: " + str(sys.getsizeof(data)))
            image += data
        print('Done Receiving!')


        image = codecs.decode(image, "hex")

        #nparr = np.fromstring(image, np.uint8)
        #image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #_, image = cv2.imencode('.jpg', image)
        #cv2.imwrite('test.jpg', image)

        # send image
        image_base_64 = base64.b64encode(image)
        post_image(image_base_64)




class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


print("Socket listening on {}:{}".format(HOST, PORT))
server = ThreadedTCPServer((HOST, PORT), CameraTCPHandler)
server.serve_forever()
