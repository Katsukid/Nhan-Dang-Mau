import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('IMG3.jpg')
tmp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(tmp)
plt.show()
def getTwoSmallest(arr):
    min1, min2 = float('inf'), float('inf')
    tmp = arr.copy()
    l = tmp.__len__()
    for i in range(0, l):
        if tmp[i] > 0:
            min1 = i - 10
            break
    tmp = np.flip(tmp)
    for i in range(0, l):
        if tmp[i] > 0:
            min2 = 250 - i
            break
    return min1, min2

def removeBackGround(img):
    h, w = img.shape[:2]
    tempH = int(0.8 * h)
    tempW = int(0.3 * w)
    tempBG = img[tempH:h, 0:tempW]
    histr = []
    maxH = []
    minH = []
    for i in range(0,3):
        histr.append(cv2.calcHist([tempBG],[i],None,[256],[0,256]))
        y, x = getTwoSmallest(histr[i])
        maxH.append(x)
        minH.append(y)
    # print(maxH, minH)
    for x in range (0, h):
        for y in range(0, w):
            v = img[x][y][0] - img[x][y][1]
            tmp12 = np.abs(v) 
            tmp23 = np.abs(img[x][y][1] - img[x][y][2])
            tmp31 = np.abs(img[x][y][2] - img[x][y][0])
            if (tmp12 >= 35) \
            or (tmp23 >= 35) :
                img[x][y] = [255, 255, 255]
                # print(img[x][y])
    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(tmp)
    plt.show()
    cv2.imwrite('temp3.jpg',img)
removeBackGround(img)
# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv2.calcHist([bg],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
# plt.show()
# for i in range(0,3):
#     img[]

