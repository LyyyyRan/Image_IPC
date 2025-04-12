# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 22:35:06 2025

@author: LyyyyRan
"""

from __future__ import print_function

import cv2 as cv
import numpy as np
from multiprocessing import shared_memory

# Topic Name:
topic_name = 'LyyyyRan::Camera'

# Just temp:
image = None
memory = None

# Get Params of Image && Msg:
image_height = int(480)  # Height
image_width = int(640)  # Width
image_channel = 3  # OpenCV-Python::BGR
image_dtype = np.uint8  # DateType: uint
image_shape = (image_height, image_width, image_channel)  # Shape
image = np.zeros(shape=image_shape, dtype=image_dtype)  # image temp
image_size = image.nbytes  # Image Size: size of MSGs for IPC

# Get the Existing Memory by the name:
try:
    memory = shared_memory.SharedMemory(name=topic_name, create=False)
except Exception as e:
    print('Lyyy Err:', e)
    print('Lyyy Warning: Never Creat Subscribers before the Publisher!!!')
    exit()

# Main:
while True:
    try:
        image = np.ndarray(shape=image_shape, dtype=image_dtype, buffer=memory.buf)  # Subscribe Msgs from the Topic
    except Exception as e:
        print('Lyyy Error:', e)

    # Main Work:
    if image is not None:
        # Ask one window to Show image:
        cv.imshow('from Shared Memory', image)

        # whether to stop process:
        if cv.waitKey(1) == ord(' '):
            print('Lyyy: Keyboard Interrupt!')
            break
    else:
        print('Lyyy: Failed to Read from the memory!')
        break

# Destroy this window:
cv.destroyWindow('from Shared Memory')

if __name__ == '__main__':
    pass
