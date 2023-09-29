import cv2
import numpy as np

# 1. FIND THE COORDINATES 
# 2. WRITE THE COORDINATES TO A FILE
# 3. PICK A POINT WHERE YOU WANT TO START
# 4. START SEARCHING

# Q: SHOULD WE CHANGE THE COORDINATES WHERE WE FOUND A PIXEL TO A SPECIFIC VALUE E.G. 1 AND MANUALLY ADD VALUES REP WHITE E.G. 0 IN BETWEEN?



image = cv2.imread('/Users/joeycheng/Desktop/filt/filtering_v2/final_equal_erode_dilate.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # WHAT DOES THIS LINE DO?

# Set threshold level
threshold_level = 255 # WELL, IT'S ACTUALLY A POINT..

# Find coordinates of all pixels below threshold
coords = np.column_stack(np.where(gray = threshold_level))

print(coords)

# Create mask of all pixels lower than threshold level
mask = gray < threshold_level

# Color the pixels in the mask
gray[mask] = (204, 119, 0)

cv2.imshow('image', image)
cv2.waitKey()