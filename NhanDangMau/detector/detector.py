import cv2
import numpy as np
import statistics
import copy
import pytesseract
from PIL import Image
from util.util import get_contour_boxes, get_img_from_box, get_threshold_img, find_max_box, show_img, draw_rec, plot_img
from util.resize import resize_img_by_height, resize_img_by_width
from matplotlib import pyplot as plt
def plot_img(img):
    plt.imshow(img)
    plt.show()

def cropout_unimportant_part(img):
    h, w, _ = img.shape
    x = get_information_x_axis(img)
    y = get_information_y_axis(img)
    pic = img[int(1.2*y):int(0.9*h), 0:int(0.9 * x)]
    img = img[y:h, x:w]

    return img, pic


def crop_label(img):
    h, w, _ = img.shape
    img = img[0:int(0.9*h), 0:int(0.1 * w)]
    return img


def get_info_list(img, contour_boxes):
    contour_boxes.sort(key=lambda tup: tup[1])
    height, width, _ = img.shape
    list_info = []
    for index, l in enumerate(contour_boxes):
        x, y, w, h = l
        y = y - 20
        if index != len(contour_boxes) - 1:
            x1, y1, _, _ = contour_boxes[index+1]
            list_info.append((x, y, width, y1))
        else:
            list_info.append((x, y, width, height))
    return list_info


def get_main_text(img, box, kernel_height):
    x0, y0, x1, y1 = box
    img = img[y0:y1, x0:x1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    thresh = get_threshold_img(img, kernel)
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (thresh.shape[1], kernel_height))
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    contour_boxes = get_contour_boxes(dilation)
    max_box = max(contour_boxes, key=lambda tup: tup[2] * tup[3])
    x, y, w, h = max_box
    return (x0+x, y0+y, x0+x+w, y0+y+h)


def remove_name_label(group, width):
    avg = statistics.mean(map(lambda t: t[-1], group))
    group_orig = copy.deepcopy(group)
    for element in group_orig:
        if element[0] < width/10:
            group.remove(element)
        elif element[-1] < avg and element[0] < width/5:
            group.remove(element)
    return group


def remove_smaller_area(group, width):
    avg = statistics.mean(map(lambda t: t[-1] * t[-2], group))
    group_orig = copy.deepcopy(group)
    for element in group_orig:
        if element[0] < width/10:
            group.remove(element)
        elif element[-1] * element[-2] < avg and element[0] < width/5:
            group.remove(element)
    return group


def get_name(img, box):
    x0, y0, x1, y1 = box
    img = img[y0:y1, x0:x1]
    height, width, _ = img.shape
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    thresh_img = get_threshold_img(img, kernel)
    contour_boxes = get_contour_boxes(thresh_img)
    contour_boxes = remove_smaller_area(contour_boxes, width)
    contour_boxes = remove_name_label(contour_boxes, width)
    contour_boxes.sort(key=lambda t: t[0])
    x, y, w, h = find_max_box(contour_boxes)
    return (x0+x, y0+y, x0+x+w, y0+y+h)


def get_text_from_two_lines(img, box):
    x0, y0, x1, y1 = box
    img = img[y0:y1, x0:x1]
    kernel = np.ones((25, 25), np.uint8)
    thresh = get_threshold_img(img, kernel)
    height, width = thresh.shape
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    contour_boxes = get_contour_boxes(dilation)
    avg = statistics.mean(map(lambda t: t[-1]*t[-2], contour_boxes))
    boxes_copy = copy.deepcopy(contour_boxes)
    for box in boxes_copy:
        box_height = box[1] + box[3]
        height_lim = 0.9 * height
        if box[1] > height_lim:
            contour_boxes.remove(box)
        elif box_height == height and box[1] > 0.8 * height:
            contour_boxes.remove(box)
        elif box[-1] * box[-2] < avg/3:
            contour_boxes.remove(box)
    x, y, w, h = find_max_box(contour_boxes)
    if h < 55:
        return (x0+x, y0+y, x0+x+w+5, y0+y+h+5)
    else:
        crop_img = thresh[y:y+h, x:width]
        height, width = crop_img.shape
        hist = cv2.reduce(crop_img, 1, cv2.REDUCE_AVG).reshape(-1)
        hist = uppers = [hist[y] for y in range(height//3, 2*height//3)]
        line = uppers.index(min(uppers)) + height//3
        temp1 = int((y0+y)*0.98)
        temp3 = int((y0+y+line)*1.01)
        first_line = (x0+x, temp1, x0+x+w+5, temp3)
        second_line = (x0+x, temp3-3, x0+x+w+5, int((temp1+h+5)))
        return [first_line, second_line]


def get_two_lines_img(img, box):
    x0, y0, x1, y1 = box
    img = img[y0:y1, x0:x1]
    kernel = np.ones((25, 25), np.uint8)
    thresh = get_threshold_img(img, kernel)
    height, width = thresh.shape
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    contour_boxes = get_contour_boxes(dilation)
    avg = statistics.mean(map(lambda t: t[-1]*t[-2], contour_boxes))
    boxes_copy = copy.deepcopy(contour_boxes)
    for box in boxes_copy:
        box_height = box[1] + box[3]
        height_lim = 0.9 * height
        if box[1] > height_lim:
            contour_boxes.remove(box)
        elif box_height == height and box[1] > 0.8 * height:
            contour_boxes.remove(box)
        elif box[-1] * box[-2] < avg/3:
            contour_boxes.remove(box)
    x, y, w, h = find_max_box(contour_boxes)
    return (x0+x, y0+y, x0+x+w+5, y0+y+h+5)


def process_result(orig, ratio, result):
    if type(result) is tuple:
        return [get_img_from_box(orig, ratio, result, padding=2)]
    if type(result) is list:
        first_line = get_img_from_box(orig, ratio, result[0], padding=2)
        first_line = cut_blank_part(first_line)
        second_line_img = get_img_from_box(orig, ratio, result[1], padding=2)
        second_line = cut_blank_part(second_line_img)
        return [first_line, second_line]


def get_last_y(result):
    if type(result) is tuple:
        return result[-1]
    if type(result) is list:
        return result[1][-1]


def cut_blank_part(img, padding=5):
    img_h, img_w, _ = img.shape
    kernel = np.ones((25, 25), np.uint8)
    thresh = get_threshold_img(img, kernel)
    contour_boxes = get_contour_boxes(thresh)
    avg = statistics.mean(map(lambda t: t[-1], contour_boxes))
    boxes_copy = copy.deepcopy(contour_boxes)
    for box in boxes_copy:
        if box[-1] < avg/2:
            contour_boxes.remove(box)
        elif box[1] > img_h/2 and box[0] < img_w/10:
            contour_boxes.remove(box)
        elif box[1] < img_h/10 and box[-1] < img_h/5:
            contour_boxes.remove(box)
    x, y, w, h = find_max_box(contour_boxes)
    new_width = x + w + padding
    if new_width > img_w:
        new_width = img_w
    return img[0:img_h, x: new_width]


def get_information_x_axis(img):
    img, ratio = resize_img_by_height(img)
    h, w, _ = img.shape
    img_resize = img[100:400, int(0.25*w):int(0.4*w)]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))
    thresh = get_threshold_img(img_resize, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, h))
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    cnts = get_contour_boxes(dilation)
    cnts_copy = copy.deepcopy(cnts)
    for cnt in cnts_copy:
        if cnt[0] < 0.1*img_resize.shape[1]:
            cnts.remove(cnt)
    max_cnt = max(cnts, key=lambda x: x[-1] * x[-2])
    return int((max_cnt[0]-5+0.25*w)*ratio)


def get_information_y_axis(img):
    img, ratio = resize_img_by_width(img)
    h, w, _ = img.shape
    img_resize = img[0:int(0.4*h), 125:w]
    gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((25, 25), np.uint8)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    thresh = cv2.threshold(
        blackhat, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    cnts = get_contour_boxes(dilation)
    cnts_copy = copy.deepcopy(cnts)
    for cnt in cnts_copy:
        if cnt[1]+cnt[-1] > 0.95 * img_resize.shape[0]:
            cnts.remove(cnt)
        elif cnt[-2] < 150:
            cnts.remove(cnt)
    max_cnt = max(cnts, key=lambda x: x[1])
    return int((max_cnt[1]-5)*ratio)


def detect_info(img):
    img, face = cropout_unimportant_part(img)
    # plot_img(img)
    orig = img.copy()
    img, ratio = resize_img_by_height(img)
    label_img = crop_label(img)
    # plot_img(label_img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    threshold_img = get_threshold_img(label_img, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (label_img.shape[1]//2, 5))
    dilation = cv2.dilate(threshold_img, kernel, iterations=1)
    # plot_img(dilation)
    contour_boxes = get_contour_boxes(dilation)
    contour_boxes.sort(key=lambda t: t[2] * t[3], reverse=True)
    contour_boxes = contour_boxes[:5]
    info_list = get_info_list(img, contour_boxes)
    # get number part
    x, y, _, _ = info_list[0]
    number_box = (0, 0, img.shape[1], info_list[0][1])
    number_box = get_main_text(img, number_box, 5)
    number_img = get_img_from_box(orig, ratio, number_box)
    # get name part
    name_box = info_list[0]
    name_box = get_name(img, get_main_text(img, name_box, 5))
    name_img = get_img_from_box(orig, ratio, name_box, padding=2)    
    # plot_img(name_img)
    tmpls = list(name_box)
    tmpls[1] = int(tmpls[1] * 0.9) # Keo len 1 chut de tranh mat dau
    tmpls[3] = int(tmpls[3] * 1.1) # Keo xuong 1 chut de tranh mat dau
    tmpls[0] = int(tmpls[0] * 0.99) # Keo len 1 chut de tranh mat dau
    tmpls[2] = int(tmpls[2] * 1.01) # Keo xuong 1 chut de tranh mat dau
    name_box = tuple(tmpls)
    name_img = get_img_from_box(orig, ratio, name_box, padding=2)    
    # plot_img(name_img)
    # name_img = cut_blank_part(name_img)
    # get dob part
    dob_box = info_list[1]
    dob_box = get_main_text(img, dob_box, 5)
    # dob_img = get_img_from_box(orig, ratio, dob_box)
    # plot_img(dob_img)
    tmpls = list(dob_box)
    tmpls[1] = int(tmpls[1] * 0.99) # Gian no len 1
    tmpls[3] = int(tmpls[3] * 1.01) # Gian no xuong 1
    # tmpls[0] = int(tmpls[2] * 0.3) # Cat phan chu di
    dob_box = tuple(tmpls)
    dob_img = get_img_from_box(orig, ratio, dob_box)
    # plot_img(dob_img)
    # get gender_and national part
    gender_and_nationality_box = info_list[2]
    gender_and_nationality_box = get_main_text( img, gender_and_nationality_box, 5)
    # gender_n_nation_img = get_img_from_box( orig, ratio, gender_and_nationality_box, padding=2)
    # plot_img(gender_n_nation_img)
    tmpls = list(gender_and_nationality_box)
    tmpls[1] = int(tmpls[1] * 0.99) # Gian no len 1
    tmpls[3] = int(tmpls[3] * 1.01) # Gian no xuong 1
    gender_and_nationality_box = tuple(tmpls)
    gender_n_nation_img = get_img_from_box( orig, ratio, gender_and_nationality_box, padding=2)
    # plot_img(gender_n_nation_img)
    h, w, _ = gender_n_nation_img.shape
    gender_img = gender_n_nation_img[0:h, 0:int(w/3)]
    # plot_img(gender_img)
    nation_img = gender_n_nation_img[0:h, int(w/3):int(w)]
    # plot_img(nation_img)
    nation_img = cut_blank_part(nation_img)
    # plot_img(nation_img)
    # get country part
    country_box = info_list[3]
    x, y, x1, y1 = country_box
    last_y = gender_and_nationality_box[-1]
    country_img = process_result(
        orig, ratio, get_two_lines_img(img, (x, int(last_y+3), x1, int(y1+3))))[0]
    country_result = get_text_from_two_lines(img, (x, int(last_y+3), x1, int(y1+3)))
    # plot_img(country_img)
    country_img_list = process_result(orig, ratio, country_result)
    # for y in range(len(country_img_list)):
    #     plt.subplot(len(country_img_list), 1, y+1)
    #     plt.imshow(country_img_list[y])
    # plt.show()
    address_box = info_list[4]
    x, y, x1, y1 = address_box
    last_y = get_last_y(country_result)
    address_img = process_result(
        orig, ratio, get_two_lines_img(img, (x+40, last_y, x1, y1)))[0]
    # plot_img(address_img)
    result = get_text_from_two_lines(img, (x+40, last_y, x1, y1))
    address_img_list = process_result(orig, ratio, result)
    # for y in range(len(address_img_list)):
    #     plt.subplot(len(address_img_list), 1, y+1)
    #     plt.imshow(address_img_list[y])
    # plt.show()
    return face, number_img, name_img, dob_img, gender_img, nation_img, country_img, \
        address_img, country_img_list, address_img_list
#(x, y, width, height)