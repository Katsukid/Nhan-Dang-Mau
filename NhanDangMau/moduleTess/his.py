import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse
import os
def plot_img(img):
    plt.imshow(img)
    plt.show()
folder = "image2"
originFolder = folder 
clearBackgroundFolder = folder + "\\clearBG"
if not os.path.exists(clearBackgroundFolder):
    os.makedirs(clearBackgroundFolder)
lsImg = [originFolder +"\\" + x for x in os.listdir(originFolder) if x.endswith(".jpg")]
imgbase = cv2.imread('image2\\7.jpg', 0)

def find_nearest_above(my_array, target):
    diff = my_array - target
    mask = np.ma.less_equal(diff, -1)
    # We need to mask the negative differences
    # since we are looking for values above
    if np.all(mask):
        c = np.abs(diff).argmin()
        return c # returns min index of the nearest if target is greater than any value
    masked_diff = np.ma.masked_array(diff, mask)
    return masked_diff.argmin()
def hist_match(original, specified):
     
    oldshape = original.shape
    original = original.ravel()
    specified = specified.ravel()
 
    # get the set of unique pixel values and their corresponding indices and counts
    s_values, bin_idx, s_counts = np.unique(original, return_inverse=True,return_counts=True)
    t_values, t_counts = np.unique(specified, return_counts=True)
 
    # Calculate s_k for original image
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    
    # Calculate s_k for specified image
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]
 
    # Round the values
    sour = np.around(s_quantiles*255)
    temp = np.around(t_quantiles*255)
    
    # Map the rounded values
    b=[]
    for data in sour[:]:
        b.append(find_nearest_above(temp,data))
    b= np.array(b,dtype='uint8')
 
    return b[bin_idx].reshape(oldshape)

for i in lsImg:
    image1 = cv2.imread(i)
    img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 
    # h, w = img.shape[:2]
    # for x in range (0, h):
    #     for y in range(0, w):
    #         if img[x][y] >= 40:
    #             img[x][y] = 255
    #         else:
    #             img[x][y] = 0
    # thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #          cv2.THRESH_BINARY,11,2)
    # a = hist_match(img, imgbase)

    # ret, thresh2 = cv2.threshold(res, 90, 255, cv2.THRESH_BINARY_INV) 
    ret, thresh = cv2.threshold(img, 80, 255, cv2.THRESH_TRUNC)
    
    cv2.imwrite(i.replace("\\","\\clearBG\\"),thresh)
    print(i.replace("\\","\\clearBG\\"))
