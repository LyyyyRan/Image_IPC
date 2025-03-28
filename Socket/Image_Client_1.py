from __future__ import print_function

import socket
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
window_toShow = 'Client1_RecvFromServer'  # named a window to show image
msg_toServer = 'dd'
msg_size = getsizeof(msg_toServer)

# get socket:
socket_client = socket.socket()

# connect by ip addr && port:
socket_client.connect(("localhost", 8888))

# Set msg size:
socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, image_size)
socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, msg_size)

# Keep ask img from Server:
while True:
    # Send any words except 'X'
    send_msg = msg_toServer

    # ask for image:
    try:
        socket_client.send(send_msg.encode("UTF-8"))
    except Exception as e:
        print(e)
        cv.waitKey(20)  # delay 20 ms
        socket_client = socket.socket()
        socket_client.connect(("localhost", 8888))
        socket_client.send(send_msg.encode("UTF-8"))

    try:
        # keep waiting until get response:
        recv_data = socket_client.recv(image_size)  # unicode string
    except Exception as e:
        recv_data = 'ERROR'.encode('UTF-8')
        print(e)

    # transform str to np.array && set dtype tobe uint8:
    image_unicode = np.fromstring(recv_data, np.uint8)

    # decode, transform unicode to be cv::image
    image = cv.imdecode(image_unicode, 1)

    # show image:
    try:
        cv.imshow(window_toShow, image)
    except Exception as e:
        print(e)

    if cv.waitKey(1) == ord(' '):
        print('LyyyyRan: Keyboard Interrupt')
        break

# tell server to stop work:
try:
    socket_client.send('X'.encode("UTF-8"))
except Exception as e:
    print(e)
    cv.waitKey(20)  # delay 20 ms
    socket_client = socket.socket()
    socket_client.connect(("localhost", 8888))
    socket_client.send('X'.encode("UTF-8"))

# kill client:
socket_client.close()

# destroy window:
cv.destroyAllWindows()

if __name__ == '__main__':
    pass
