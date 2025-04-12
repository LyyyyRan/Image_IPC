# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 21:55:20 2025

@author: LyyyyRan
"""

from __future__ import print_function

import cv2 as cv
import numpy as np
from multiprocessing import shared_memory

# Get Camera:
cap = cv.VideoCapture(0)

# Topic Name:
topic_name = 'LyyyyRan::Camera'

# Get Params of Image && Msg:
image_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))  # Height
image_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))  # Width
image_channel = 3  # OpenCV-Python::BGR
image_dtype = np.uint8  # DateType: uint
image_shape = (image_height, image_width, image_channel)  # Shape
image = np.zeros(shape=image_shape, dtype=image_dtype)  # image temp
image_size = image.nbytes  # Image Size: size of MSGs for IPC

# print sth. Head
print('*' * 16, end=' ')
print('Echo Some Parameters', end=' ')
print('*' * 16)

print('Topic Name:', topic_name)
print('Height:', image_height)
print('Width:', image_width)

print('*' * 19, end=' ')
print('Echo Completed', end=' ')
print('*' * 19)
# print sth. End

# Create one shared memory:
memory = shared_memory.SharedMemory(name=topic_name, create=True, size=image_size)

# Get buffer of the memory:
buffer = np.ndarray(shape=image_shape, dtype=image_dtype, buffer=memory.buf)

# Main:
while True:
    flag, image = cap.read()  # Read from Camera

    # Main Work:
    if flag:
        try:
            buffer[:] = image[:]  # Send Msg to the Topic
        except Exception as e:
            print('Lyyy Err:', e)
            print('Lyyy Warning: Never Creat Subscribers before the Publisher!!!')
    else:
        print('LyyyyRan: Failed to Read')
        break

# free the camera:
cap.release()

# clear && release:
memory.close()
memory.unlink()

# Run:
if __name__ == '__main__':
    pass
