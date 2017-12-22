import socket
import sys
import base64
from threading import *
import requests
import os


# Listen on
HOST = '0.0.0.0'
PORT = 9000

# Heimdall API URL
HEIMDALL_BACKEND = os.environ.get('HEIMDALL_BACKEND')

print("Heimdall-Backend: {}".format(HEIMDALL_BACKEND))

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


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    image = ''
    while True:
        # Receiving from client
        data = conn.recv(4096)
        if not data:
            break
        image += data

    # came out of loop
    conn.close()

    # send image
    url = HEIMDALL_BACKEND + '/api/live/'
    data = {'image': base64.b64encode(image.decode("hex")), 'annotate': 'True'}
    requests.post(url, data=data)


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))

s.close()
