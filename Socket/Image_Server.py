# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 15:48 2025

@author: https://github.com/LyyyyRan/Image_IPC.git
"""

from __future__ import print_function

import socket
import threading
import cv2 as cv
import numpy as np
from sys import getsizeof

# Get Params of Image && Msg:
image_height = int(480)  # Height
image_width = int(640)  # Width
image_channel = 3  # OpenCV-Python::BGR
image_dtype = np.uint8  # DateType: uint
image_shape = (image_height, image_width, image_channel)  # Shape
image = np.zeros(shape=image_shape, dtype=image_dtype)  # image temp
image_size = image.nbytes  # Image Size: size of MSGs for IPC
msg_fromClient = 'dd'
msg_size = getsizeof(msg_fromClient)

# temp value for connection && id:
conn = None
conn_id = 0

# get camera:
cap = cv.VideoCapture(0)

# get socket:
socket_server = socket.socket()

# bind ip host && port:
socket_server.bind(("localhost", 8888))

# Start to listen && Set the maximum number of connections to 5.
socket_server.listen(5)

# Set timeout && msg size:
socket.setdefaulttimeout(20)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, msg_size)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, image_size)


# callback for multi-threading:
def callback(connect):
    # using golbal value:
    global socket_server, image

    while True:
        # receive data:
        try:
            data_from_client = connect.recv(1024).decode("UTF-8")
        except Exception as e:
            print(e)
            data_from_client = 'dd'  # default value
            print('Failed to Recv')

        # whether to stop work:
        if 'X' in data_from_client:  # set a stop flag
            print('LyyyyRan: Stop the Service && Exit')
            break
        else:
            # read camera:
            flag, image = cap.read()

            # succeed:
            if flag:
                # encode && transform tobe string:
                image_unicode = cv.imencode('.jpg', image)
                str_unicode = image_unicode[1].tostring()

                # send img_str in utf-8:
                try:
                    cv.waitKey(1)  # delay

                    connect.send(str_unicode)  # response
                    print('LyyyyRan: Send image')
                except Exception as e:
                    print(e)
                    socket_server = socket.socket()  # ReInit
                    socket_server.bind(("localhost", 8888))
                    socket_server.listen(5)
            else:
                print('Failed to read image from camera')
                break

    # close connections && service:
    connect.close()
    socket_server.close()

    # release camera:
    cap.release()

    # exit python:
    exit()


# echo work status:
print('Start Working...')

# Main Work:
while True:
    conn_id += 1  # new connection

    # keep waiting until someone connect:
    conn, address = socket_server.accept()

    # echo the addr of client:
    print('receive msg from' + str(address))

    client_handler = threading.Thread(target=callback, args=(conn,))
    client_handler.start()
