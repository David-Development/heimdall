import cv2
import base64
import sys
from urllib import request, parse
import time
import urllib.error
import socket
import os

RTSP_HOST_IP = os.environ['RTSP_HOST']

HEIMDALL_HOST = 'http://heimdall'
HEIMDALL_PORT = 5000
frame_count = 0

print("Let server finish starting")
time.sleep(12)
print("Okay, let's go!")

url = "rtsp://{}:8554/unicast".format(RTSP_HOST_IP)
print("Connecting to host: {}".format(url))
vcap = cv2.VideoCapture(url)

while True:
    ret, frame = vcap.read()

    # cv2.imshow('VIDEO', frame)
    # cv2.waitKey(1)

    if ret and (frame_count % 5) == 0:
        print("Send request to server!")
        cnt = cv2.imencode('.jpg', frame)[1]
        b64 = base64.b64encode(cnt)

        url = HEIMDALL_HOST + ":" + str(HEIMDALL_PORT) + '/api/live/'
        data = {'image': b64, 'annotate': 'True'}

        print("Url:", url)

        data = parse.urlencode(data).encode()

        print("Data encoded")

        req = request.Request(url, data=data) # this will make the method "POST"

        print("Requesting now!")

        try:
            resp = request.urlopen(req, timeout=2)
        except urllib.error.URLError as e:
            print("urllib.error.URLError", e)
        except socket.timeout as e:
            print("socket.timeout", e)

        # time.sleep(2)

    frame_count += 1

print("Shutdown..")
