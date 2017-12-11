import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish 
import time 
import logging 
import os
import base64 

def post_image(file_name): 
    print("============")
    print('Taking photo') 
   
    with open(file_name, "rb") as imageFile: 
       image_read = imageFile.read() 
       data = base64.encodestring(image_read)
       #data = bytearray(image_read) 
    (result, mid) = client.publish("camera", data, mqttQos, mqttRetained)
    print(file_name + ' - image published') 
    print(result, ' - ', mid)

### MQTT 
broker = 'mqtt-broker' 
topic ='trigger' 
mqttQos = 0
mqttRetained = False 


fileList = os.listdir("images")

#
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    client.subscribe(topic) 
    

# The callback for when a PUBLISH message is received from the server.
# 
def on_message(client, userdata, msg): 
    print("=========")
    payload = str(msg.payload.decode('ascii'))  # decode the binary string 
    print("on_message: " + msg.topic + " " + payload) 
    process_trigger(payload) 
#
def process_trigger(payload): 
    if payload == 'ON': 
        print('ON triggered') 

        if len(fileList) > 0:
            post_image("./images/{}".format(fileList.pop()))


def on_publish(client, obj, mid):
    print("=========")
    print("Publish - Mid:", mid)

def on_log(client, userdata, level, buf):
    print(level, buf)

def on_disconnect(client, userdata, rc):
    print("=========")
    print("Disconnected:", mqtt.connack_string(rc))


#
client = mqtt.Client(client_id="heimdall-test")  # protocol=mqtt.MQTTv31

client.on_connect = on_connect    # call these on connect and on message 
client.on_message = on_message
client.on_publish = on_publish 
client.on_disconnect = on_disconnect
#client.on_log = on_log

#client.username_pw_set(username='user',password='pwd')  # need this 
client.connect(broker, 1883, 60) 
client.loop_forever()    #  don't get past this 
#client.loop_start()    #  run in background and free up main thread
