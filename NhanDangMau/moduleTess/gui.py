import cv2
import pytesseract
import numpy as np
from PIL import Image
import re
import subprocess
import copy
import statistics
import math
from unidecode import unidecode
from util.util import get_threshold_img, get_contour_boxes, run_item, gather_results
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Katsukid\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

def get_text(img):
    filename = 'temp.png'
    config = ''
    lang = 'vie'
    cv2.imwrite(filename, img)
    text = pytesseract.image_to_string(Image.open(
        filename), lang=lang, config=config)
    print(text)
    temp = text.split(':')
    if temp.__len__() >= 2:
        text = temp[1]
    else:
        text = temp[0]
    return text
img = cv2.imread('image2\\clearBG\\72.jpg',0)
get_text(img)
