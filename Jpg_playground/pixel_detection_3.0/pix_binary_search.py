import cv2
import numpy as np
import operator

import time
from datetime import timedelta

start_time = time.monotonic()

STARTING_POINT = [200,675] # [X,Y] IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices
ALL_GREY_PIX = [] # SAVE AS [X,Y] COORDINATES
LEFT_PIX = []
RIGHT_PIX = []

image = cv2.cvtColor(cv2.imread('images/filtered_slam_map.jpg'), cv2.COLOR_BGR2GRAY) 
threshold_level = 0
coordinates_yx = np.column_stack(np.where(image == threshold_level))
coordinates_xy = np.fliplr(coordinates_yx)

np.savetxt("np_array.txt", coordinates_xy) # POSSIBLE TO CHANGE THE COORDINATES IN THE FILE FROM SCIENTIFIC NOTATION TO INTEGERS?


# BINARY SEARCH 
arr = coordinates_xy

def binarySearch(arr, l, r, x):
    while l <= r:
        mid = l + (r - l) // 2
        if arr[mid][1] == x:
            return True
        elif arr[mid][1] < x:
            l = mid + 1
        else:
            r = mid - 1
    return False

# OLD CODE
def first_pix(op): 
    y_coordinate = op(STARTING_POINT[1], 1)
    inArray = binarySearch(arr, 0, len(arr)-1, y_coordinate)

    while True:
        if inArray: 
            FIRST_PIX = [STARTING_POINT[0], op(y_coordinate, 10)]
            return FIRST_PIX
        else:
            y_coordinate = op(y_coordinate, 1)
            inArray = binarySearch(arr, 0, len(arr)-1, y_coordinate)


# THE REST OF THE CODE
def first_grey_pix():
    first_right_pix = first_pix(operator.add)
    print(f"FIRST RIGHT PIX: {first_right_pix}")
    RIGHT_PIX.append(first_right_pix)
    first_left_pix = first_pix(operator.sub)
    LEFT_PIX.append(first_left_pix)
    ALL_GREY_PIX.extend((STARTING_POINT,first_right_pix, first_left_pix))
    return ALL_GREY_PIX

# THE REST OF THE REST OF THE CODE
def left_line(op):
    x_coordinate = LEFT_PIX[-1][0]
    y_coordinate = LEFT_PIX[-1][1]

    x = LEFT_PIX[-1][0]
    x_coordinate = op(x_coordinate, 100) 
    inArray = binarySearch(arr, 0, len(arr)-1, x)
    for i in range(3):
        if inArray: 
            LEFT_PIX.append([x_coordinate, y_coordinate])   
            ALL_GREY_PIX.append([x_coordinate, y_coordinate])
        else:
            x_coordinate = op(x_coordinate, 100) 
            inArray = binarySearch(arr, 0, len(arr)-1, x_coordinate)


def swap_index(L):
    for i in L:
        i[0], i[1] = i[1], i[0]
    return L

def colour_ALL_GREY_PIX(): # HAVE TO COLOUR IN AS [Y,X] COORDINATES
    L = ALL_GREY_PIX
    swapped = swap_index(L)
    for i in swapped:
        image[(i[0],i[1])] = 100

def run():
    first_grey_pix()



run()
print(ALL_GREY_PIX) 
print(f"LEFT PIX: {LEFT_PIX}")
print(f"RIGHT PIX: {RIGHT_PIX}")


end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))

def show_on_photo():
    colour_ALL_GREY_PIX()
    cv2.imwrite('images/image_pix.jpg', image)

show_on_photo()



