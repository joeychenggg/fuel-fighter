import cv2 as cv
import numpy as np

# BLUR
img = cv.imread('img.jpg')
# img_bf = cv.GaussianBlur(img,(9,9),0)

# FILTER
img[img >= 100] = 255 
img[img < 100] = 0
# img_bf[img_bf >= 100] = 255 
# img_bf[img_bf < 100] = 0
cv.imwrite('img_blurred_and_filtered.jpg', img)

# DILATE AND ERODE
img = cv.imread('img_blurred_and_filtered.jpg', -1)
kernel = np.ones((21,21),np.uint8)

erosion = cv.erode(img,kernel,iterations = 2) # AS THE BACKGROUND IS WHITE INSTEAD OF BLACK, CALLING CV.ERODE() WILL DILATE THE PHOTO
dilation = cv.dilate(erosion,kernel,iterations = 1) # -- ERODE THE PHOTO

cv.imwrite('final_equal_erode_dilate.jpg', dilation)
