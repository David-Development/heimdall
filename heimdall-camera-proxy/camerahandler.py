import socket
import sys
import base64
import threading
import requests
import os
import codecs

# Listen on
HOST = ''
PORT = 9000

### MQTT 
#broker = 'mqtt-broker' 
broker = os.environ.get('MQTT_BROKER_IP')
topic ='trigger' 
mqttQos = 0
mqttRetained = False 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket created')

# Bind socket to local host and port
try:
    print("Binding socket to host...")
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# Start listening on socket
s.listen(10)
print("Socket now listening on {}:{}".format(HOST, PORT))



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
    process_trigger(payload) 

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
client.connect(broker, 1883, 60) 
# client.loop_forever()    #  don't get past this 
client.loop_start()    #  run in background and free up main thread





# Function for handling connections. This will be used to create threads
def clientthread(conn):
    image = b''
    while True:
        # Receiving from client
        data = conn.recv(4096)
        if not data:
            break
        image += data

    # came out of loop
    conn.close()

    # send image
    image_base_64 = base64.b64encode(codecs.decode(image, "hex"))
    post_image(image_base_64)


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    #start_new_thread(clientthread, (conn,))
    threading.Thread(
        target=clientthread,
        args=(conn,),
    ).start()

s.close()
