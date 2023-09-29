import cv2
import numpy as np

image = cv2.imread('/Users/joeycheng/Desktop/filt/filtering_v2/final_equal_erode_dilate.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Set threshold level
threshold_level = 200

# Find coordinates of all pixels below threshold
coords = np.column_stack(np.where(gray < threshold_level))

print(coords)
# print(len(coords))

### USE THE CODE BELOW TO VISUALIZE THE COORDINATES WHICH WE WILL SEND TO THE LOCAL PATH PLANNING###
# Create mask of all pixels lower than threshold level
mask = gray < threshold_level

# Color the pixels in the mask
image[mask] = (204, 119, 0) 

cv2.imshow('image', image)
cv2.waitKey()

# a_file = open("test.txt", "w")
# for row in coords:
#     np.savetxt(a_file, row)

# a_file.close()


# np.savetxt("file2.txt", coords)