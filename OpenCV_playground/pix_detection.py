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

image = cv2.imread('images/filtered_slam_map.pgm', -1) 
# image = cv2.cvtColor(cv2.imread('images/filtered_slam_map.pgm'), cv2.COLOR_BGR2GRAY) 
threshold_level = 0
coordinates_yx = np.column_stack(np.where(image == threshold_level))
coordinates_xy = np.fliplr(coordinates_yx)


np.savetxt("np_array.txt", coordinates_xy) # POSSIBLE TO CHANGE THE COORDINATES IN THE FILE FROM SCIENTIFIC NOTATION TO INTEGERS?

def first_pix(STARTING_POINT, op): 
    y_coordinate = STARTING_POINT[1]
    while True:
        y_coordinate = op(y_coordinate, 1) # HOW DO WE KNOW THAT WE WILL MEET A BLACK PIX AS LONG AS WE WALK IN THE Y-DIRECTION?
        if [STARTING_POINT[0], y_coordinate] in coordinates_xy.tolist(): # POSSIBLE TO NOT USE A LIST TO CHECK? IS IT BETTER TO USE AN ARRAY OR A LIST?
            FIRST_PIX = [STARTING_POINT[0], op(y_coordinate, 10)] # ADD/SUBTRACT 10 TO THE Y-COORDINATE TO FIND THE MIDDLE OF THE LINE
            return FIRST_PIX

def first_grey_pix():
    first_right_pix = first_pix(STARTING_POINT, operator.add)
    RIGHT_PIX.append(first_right_pix)
    first_left_pix = first_pix(STARTING_POINT, operator.sub)
    LEFT_PIX.append(first_left_pix)
    ALL_GREY_PIX.extend((STARTING_POINT,first_right_pix, first_left_pix))
    return ALL_GREY_PIX

def left_line(op):
    x_coordinate = LEFT_PIX[-1][0]
    y_coordinate = LEFT_PIX[-1][1]
    for i in range(3):
        x_coordinate = op(x_coordinate, 100) # HOW DO WE KNOW IF THE Y-COORDINATE IS TOWARDS "NORTH" OR "SOUTH"?
        if [x_coordinate, y_coordinate] in coordinates_xy.tolist(): 
            LEFT_PIX.append([x_coordinate, y_coordinate])   
            ALL_GREY_PIX.append([x_coordinate, y_coordinate])


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
    left_line(operator.add)




def show_on_photo():
    colour_ALL_GREY_PIX()
    cv2.imwrite('images/image_pix.jpg', image)

run()
print(ALL_GREY_PIX) 
print(f"LEFT PIX: {LEFT_PIX}")
print(f"RIGHT PIX: {RIGHT_PIX}")


end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))

show_on_photo()