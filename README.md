# Image_IPC

# Abstract

    A demo of the IPC for images (np.ndarray), the Template for myself.

# Environmental dependence

    1) Had a better get OpenCV >= 3.0

# Catalog Structure Description

    ├── Image_Publisher.py  // Demo of pub msg
    
    ├── Image_Subscriber    // Demo of subscribe msg

    └── ReadMe.md           // Introduction

# Introduction

    1) Run Image_Publisher.py after any other Subscribers run.

# Version Update

###### v0:

    1. Via ROS::CV_Bridge, which is available for Python3 merely in ROS_Noetic (Ubuntu 20.04). 

###### v1(Now):

    1. Via multiprocessing pkg, which is available for both Python3 and Python2.
    2. Via Memory Sharing Method.