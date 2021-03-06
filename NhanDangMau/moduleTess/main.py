import argparse
import cv2
from cropper.cropper import crop_card
from detector.detector import detect_info
from reader import reader
import matplotlib.pyplot as plt
import numpy as np
import sys
import json

def show_img(img):
    cv2.imshow('', img)
    cv2.waitKey(0)


def plot_img(img):
    plt.imshow(img)
    plt.show()


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
args = vars(ap.parse_args())


img = cv2.imread(args["image"])
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plot_img(img)

warped = crop_card(args["image"])
# plot_img(warped)

if warped is None:
    print('Cant find id card in image - Cant crop')
    sys.exit()

try:
    face, number_img, name_img, dob_img, gender_img, nation_img, \
        country_img, address_img, country_img_list, address_img_list = detect_info(
            warped)
except:
    print('Cant find id card in image - Cant detect area')
    sys.exit()


list_image = [face, number_img, name_img, dob_img,
              gender_img, nation_img, country_img, address_img]

# for y in range(len(list_image)):
#     plt.subplot(len(list_image), 1, y+1)
#     plt.imshow(list_image[y])
# plt.show()
# for y in range(len(country_img_list)):
#     plt.subplot(len(country_img_list), 1, y+1)
#     plt.imshow(country_img_list[y])
# plt.show()
# for y in range(len(address_img_list)):
#     plt.subplot(len(address_img_list), 1, y+1)
#     plt.imshow(address_img_list[y])
# plt.show()

number_text = reader.get_id_numbers_text(number_img)
# plot_img(cv2.cvtColor(cv2.threshold(cv2.cvtColor(name_img,cv2.COLOR_BGR2GRAY), 90, 255, cv2.THRESH_TRUNC)[1],cv2.COLOR_GRAY2BGR))
name_text = reader.get_name_text(name_img)
dob_text = reader.get_dob_text(dob_img)
gender_text = reader.get_gender_text(gender_img)
nation_text = reader.get_nation_text(nation_img)
country_text = reader.process_list_img(country_img_list, is_country=True)
address_text = reader.process_list_img(address_img_list, is_country=False)

texts = ['Số:'+number_text,
         'Họ và tên: ' + name_text,
         'Ngày tháng năm sinh: ' + dob_text,
         'Giới tính: ' + gender_text,
         'Quốc tịch: ' + nation_text,
         'Quê quán: ' + country_text,
         'Nơi thường trú: ' + address_text, " "]
js = {'Số':number_text,
         'Họ và tên' : name_text,
         'Ngày tháng năm sinh' : dob_text,
         'Giới tính' : gender_text,
         'Quốc tịch' : nation_text,
         'Quê quán' : country_text,
         'Nơi thường trú' : address_text}

plt.figure(figsize=(8, (len(texts) * 1) + 2))
plt.plot([0, 0], 'r')
plt.axis([0, 3, -len(texts), 0])
plt.yticks(-np.arange(len(texts)))
for i, s in enumerate(texts):
    plt.text(0.1, -i-1, s, fontsize=16)
extractedLog = 'text_' + args["image"].split('\\')[1].replace('.jpg','.json')
plt.savefig('output.png', bbox_inches='tight')
# plt.show()
f = open(extractedLog, "w", encoding="utf-8")
f.write(json.dumps(js,indent=4,ensure_ascii=False))
f.close()