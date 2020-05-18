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
for i in lsImg:
    img = cv2.imread(i, 0)
    h, w = img.shape[:2]
    for x in range (0, h):
        for y in range(0, w):
            if img[x][y] >= 40:
                img[x][y] = 255
            else:
                img[x][y] = 0
    cv2.imwrite(i.replace("\\","\\clearBG\\"),img)
    print(i.replace("\\","\\clearBG\\"))
