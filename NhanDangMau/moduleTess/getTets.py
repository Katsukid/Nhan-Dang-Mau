import argparse
import cv2
from cropper.cropper import crop_card
from detector.detector import detect_info
from reader import reader
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os
originFolder = "warped"
lsImg = [originFolder +"\\" + x for x in os.listdir(originFolder) if x.endswith(".jpg")]
lsWarped = []
for i in lsImg:
    print(i)
    warped = cv2.imread(i)#crop_card(i)
    lsWarped.append(warped)
# plot_img(warped)
for warped, i in zip(lsWarped, lsImg):
    # w = 'warped_' + i.split('\\')[1]
    # cv2.imwrite(w,warped)
    if warped is None:
        continue
    try:
        face, number_img, name_img, dob_img, gender_img, nation_img, \
            country_img, address_img, country_img_list, address_img_list = detect_info(
                warped)
    except:
        print('Cant find id card in image - Cant detect area')
        continue
    try:
        list_image = [face, number_img, name_img, dob_img,
                    gender_img, nation_img, country_img, address_img]
        extractedLog = 'clean_text_' + i.split('\\')[1].replace('.jpg','.json')  
        # for y in range(len(list_image)):
        #     plt.subplot(len(list_image), 1, y+1)
        #     plt.imshow(list_image[y])
        # plt.savefig(extractedLog.replace('text','fig').replace('json','jpg'))
        number_text = reader.get_id_numbers_text(number_img)
        name_text = reader.get_name_text(name_img)
        dob_text = reader.get_dob_text(dob_img)
        gender_text = reader.get_gender_text(gender_img)
        nation_text = reader.get_nation_text(nation_img)
        country_text = reader.process_list_img(country_img_list, is_country=True)
        address_text = reader.process_list_img(address_img_list, is_country=False)
        js = {'Số':number_text,
                'Họ và tên' : name_text,
                'Ngày tháng năm sinh' : dob_text,
                'Giới tính' : gender_text,
                'Quốc tịch' : nation_text,
                'Quê quán' : country_text,
                'Nơi thường trú' : address_text }
          
        print(extractedLog)
        f = open(extractedLog, "w", encoding="utf-8")
        f.write(json.dumps(js,indent=4,ensure_ascii=False))
        f.close()
    except:
        continue