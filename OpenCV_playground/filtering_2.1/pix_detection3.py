import cv2
import numpy as np

image = cv2.imread('/Users/joeycheng/Desktop/filt/filtering_v2/final_equal_erode_dilate.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

threshold_level = 10

coords = np.column_stack(np.where(gray < threshold_level))

print(coords)
print(len(coords))

# np.savetxt("file2.txt", coords)


# array = np.array([[2.900000000000000000e+01, 4.000000000000000000e+02], [2.900000000000000000e+01, 4.010000000000000000e+02]])
# mask = (gray == array)

# Color the pixels in the mask
# gray[mask] = (204, 119, 0)


gray[29, 400]= (204, 119, 0)

cv2.imshow('image', image)
cv2.waitKey()