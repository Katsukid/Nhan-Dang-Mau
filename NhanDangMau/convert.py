import json
import base64
import cv2
data = {}
with open('image\\1.jpg', mode='rb') as file:
    img = file.read()
data['img'] = base64.encodebytes(img).decode("utf-8")

print(json.dumps(data))
