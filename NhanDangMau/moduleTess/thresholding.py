# Python programe to illustrate  
# simple thresholding type on an image 
      
# organizing imports  
import cv2  
import numpy as np
import matplotlib.pyplot as plt
def plot_img(img):
    plt.imshow(img)
    plt.show()
# path to input image is specified and   
# image is loaded with imread command  
image1 = cv2.imread('temp.png')
plot_img(image1)
# plot_img(image1)
# cv2.cvtColor is applied over the 
# image input with applied parameters 
# to convert the image in grayscale  
img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 

# plot_img(img)
# applying different thresholding  
# techniques on the input image 
# all pixels value above 120 will  
# be set to 255 
th = 90
ret, thresh1 = cv2.threshold(img, th, 255, cv2.THRESH_BINARY) 
ret, thresh2 = cv2.threshold(img, th, 255, cv2.THRESH_BINARY_INV) 
ret, thresh3 = cv2.threshold(img, th, 255, cv2.THRESH_TRUNC)
ret, thresh4 = cv2.threshold(img, th, 255, cv2.THRESH_TOZERO_INV)

thresh5 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

# the window showing output images 
# with the corresponding thresholding  
# techniques applied to the input images 
plt.figure()
plt.subplot(3,2,1)
plt.title('Binary Threshold')
plt.imshow(cv2.cvtColor(thresh1,cv2.COLOR_GRAY2BGR))
plt.subplot(3,2,2)
plt.title('Binary Threshold Inverted')
plt.imshow(cv2.cvtColor(thresh2,cv2.COLOR_GRAY2BGR))
plt.subplot(3,2,3)
plt.title('Truncated Threshold')
plt.imshow(cv2.cvtColor(thresh3,cv2.COLOR_GRAY2BGR))
plt.subplot(3,2,4)
plt.title('Set to 0')
plt.imshow(cv2.cvtColor(thresh4,cv2.COLOR_GRAY2BGR))
plt.subplot(3,2,5)
plt.title('Otsu Threshold')
plt.imshow(cv2.cvtColor(thresh5,cv2.COLOR_GRAY2BGR))
plt.subplot(3,2,6)
plt.title('Otsu Threshold')
plt.imshow(image1)
plt.show()