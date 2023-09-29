#!/usr/bin/env python
import rospy
from nav_msgs.msg import OccupancyGrid

import numpy as np
import cv2 as cv

# BEFORE FILTRATION
def map_to_matrix(lidar_map): 
    iterator = 0
    thresh = 50 # THIS VALUE CAN BE ADJUSTED
    lidar_map_width = lidar_map.info.width
    lidar_map_height = lidar_map.info.height

    matrix = np.zeros((lidar_map_height, lidar_map_width), dtype = "uint8")

    for i in lidar_map_height:
        for j in lidar_map_width:
            if (lidar_map.data[iterator] > thresh):
                matrix[j,i] = 0 
            else: 
                matrix[j,i] = 255 
            iterator += 1
    return matrix


# AFTER FILTRATION
def matrix_to_map(unfilt_matrix, filt_matrix, filt_map): 
    iterator = 0
    for i in filt_matrix.shape[1]:
        for j in filt_matrix.shape[0]:
            # IF BLACK: 
            if (filt_matrix[j, i] == 0):
                filt_map.data[iterator] = 100
            # IF WHITE
            else: 
                if (unfilt_matrix[j, i] == -1):
                    filt_map.data[iterator] = 100
                else:
                    filt_map.data[iterator] = 0
            iterator += 1
    return filt_map 
    

