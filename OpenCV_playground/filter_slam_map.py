import cv2 as cv
import numpy as np

image = cv.imread('images/slam_map.jpg')
kernel = np.ones((21,21),np.uint8)

image[image >= 100] = 255 
image[image < 100] = 0

filtered_slam_map = cv.erode(image,kernel,iterations = 1)
cv.imwrite('images/filtered_slam_map.jpg',filtered_slam_map)
