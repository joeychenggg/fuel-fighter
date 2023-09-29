import cv2
import numpy as np
import operator
import matplotlib.pyplot as plt

# DIVIDE THE ARRAY INTO SECTIONS SO THAT WE ONLY NEED TO SEARCH CERTAIN SECTIONS OF THE FULL ARRAY: LOWER THE RUNNING TIME
#Open file and save coordinates xy
image = cv2.cvtColor(cv2.imread('costmap.png'), cv2.COLOR_BGR2GRAY)
threshold_level = 0
coordinates_yx = np.column_stack(np.where(image == threshold_level))
coordinates_xy = np.fliplr(coordinates_yx)


STARTING_POINT = [200, 675] # [X,Y] IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices
#STARTING_POINT = [700, 300] #starting point 2 to try left side detection
yaw = 0 #in radian
ALL_GREY_PIX = [] # SAVE AS [X,Y] COORDINATES
LEFT_PIX = []
RIGHT_PIX = []



np.savetxt("np_array.txt", coordinates_xy) # POSSIBLE TO CHANGE THE COORDINATES IN THE FILE FROM SCIENTIFIC NOTATION TO INTEGERS?

def first_pix(STARTING_POINT, op): 
    y_coordinate = STARTING_POINT[1]
    while True:
        y_coordinate = op(y_coordinate, 1) # HOW DO WE KNOW THAT WE WILL MEET A BLACK PIX AS LONG AS WE WALK IN THE Y-DIRECTION?
        if [STARTING_POINT[0], y_coordinate] in coordinates_xy.tolist(): # POSSIBLE TO NOT USE A LIST TO CHECK? IS IT BETTER TO USE AN ARRAY OR A LIST?
            FIRST_PIX = [STARTING_POINT[0], op(y_coordinate, 10)] # ADD/SUBTRACT 10 TO THE Y-COORDINATE TO FIND THE MIDDLE OF THE LINE
            return FIRST_PIX

def first_grey_pix(list_of_grey_pix):
    first_right_pix = first_pix(STARTING_POINT, operator.add)
    RIGHT_PIX.append(first_right_pix)
    first_left_pix = first_pix(STARTING_POINT, operator.sub)
    LEFT_PIX.append(first_left_pix)
    ALL_GREY_PIX.extend((STARTING_POINT,first_right_pix, first_left_pix))
    return ALL_GREY_PIX

def swap_index(L):
    for i in L:
        i[0], i[1] = i[1], i[0]
    return L

def colour_ALL_GREY_PIX(): # HAVE TO COLOUR IN AS [Y,X] COORDINATES
    swapped = swap_index(ALL_GREY_PIX)
    for i in swapped:
        image[(i[0],i[1])] = 100



def left_line(op,angle):
    x_coordinate = LEFT_PIX[-1][0]
    y_coordinate = LEFT_PIX[-1][1]

    radius = 30   #searching radius was 30 at first
    if angle > np.pi/2:
        start_search = 2
        end_search = 5
    else:
        start_search = -2
        end_search = 2
    #only if orientation of the car is towards the right
    for i in range(22):
        for j in np.arange(start_search, end_search, 0.5): #0.5->0.1
            if [x_coordinate + int(radius * np.cos(j)), y_coordinate + int(radius * np.sin(j))] in coordinates_xy.tolist():
                x_new = x_coordinate + int(radius * np.cos(j))
                y_new = y_coordinate + int(radius * np.sin(j))
                break
            #else:
                #radius = 40

        LEFT_PIX.append([x_new, y_new])
        ALL_GREY_PIX.append([x_new, y_new])
        x_coordinate = x_new
        y_coordinate = y_new
    #for simulation purposes
    for i in range(35):
        for j in np.arange(2, 5, 0.5): #0.5->0.1
            if [x_coordinate + int(radius * np.cos(j)), y_coordinate + int(radius * np.sin(j))] in coordinates_xy.tolist():
                x_new = x_coordinate + int(radius * np.cos(j))
                y_new = y_coordinate + int(radius * np.sin(j))
                break


        LEFT_PIX.append([x_new, y_new])
        ALL_GREY_PIX.append([x_new, y_new])
        x_coordinate = x_new
        y_coordinate = y_new

def right_line(op,angle):
    x_coordinate = RIGHT_PIX[-1][0]
    y_coordinate = RIGHT_PIX[-1][1]
    radius = 30
    if angle > np.pi/2:
        start_search = 2
        end_search = 5
    else:
        start_search = -2
        end_search = 2
    for i in range(30):
        for j in np.arange(start_search,end_search, 0.5):
            if [x_coordinate + int(radius * np.cos(j)),y_coordinate + int(radius * np.sin(j))] in coordinates_xy.tolist():
                x_new = x_coordinate + int(radius * np.cos(j))
                y_new = y_coordinate + int(radius * np.sin(j))
                break

        RIGHT_PIX.append([x_new, y_new])
        ALL_GREY_PIX.append([x_new, y_new])
        x_coordinate = x_new
        y_coordinate = y_new
    #for simulation purposes
    for i in range(17):
        for j in np.arange(2, 5, 0.2):  # 0.5->0.1
            if [x_coordinate + int(radius * np.cos(j)),y_coordinate + int(radius * np.sin(j))] in coordinates_xy.tolist():
                x_new = x_coordinate + int(radius * np.cos(j))
                y_new = y_coordinate + int(radius * np.sin(j))
                break
            #error handling med hull i veien tar 20sek ekstra tid
            elif [x_coordinate + int((radius+50) * np.cos(j)),y_coordinate + int((radius+20) * np.sin(j))] in coordinates_xy.tolist():
                x_new = x_coordinate + int((radius+20) * np.cos(j))
                y_new = y_coordinate + int((radius+20) * np.sin(j))
                break

        RIGHT_PIX.append([x_new, y_new])
        ALL_GREY_PIX.append([x_new, y_new])
        x_coordinate = x_new
        y_coordinate = y_new


def run():
    first_grey_pix(ALL_GREY_PIX)
    left_line(operator.add,yaw)
    right_line(operator.add,yaw)
    #colour_ALL_GREY_PIX()
    #cv2.imwrite('cost2.png', image)


run()

#print(ALL_GREY_PIX) # THE PRINTING OF THE COORDINATES IS ALL WRONG!!!
print(LEFT_PIX)
print(RIGHT_PIX)


#Plotting the detected lines
x1,y1,x2,y2 = [],[],[],[]

for i in range(len(LEFT_PIX)):
    x1.append(LEFT_PIX[i][0])
    y1.append(abs(LEFT_PIX[i][1]-872))
for i in range(len(RIGHT_PIX)):
    x2.append(RIGHT_PIX[i][0])
    y2.append(abs(RIGHT_PIX[i][1]-872))

plt.plot(x1, y1)
plt.plot(x2,y2)
plt.show()


#Til neste gang: skifte if angle avhengig av twist message, angle for oppover



