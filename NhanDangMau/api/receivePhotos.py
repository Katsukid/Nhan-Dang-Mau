from datetime import datetime
from flask import jsonify, abort

import os
dirpath = os.getcwd()
DIR_PHOTOS = dirpath + "\\photos" # Dia chi luu lich su
if not os.path.exists(DIR_PHOTOS): # Neu khong co dia chi nay
    os.makedirs(DIR_PHOTOS) # Tao thu muc
import base64
def app(data):
    """
    /api/app/ - 
    Receive Raw data from client
    :param bimage:   bytes of image
    :return:       200 OK }
    """
    today = datetime.now().today()
    cur_time = today.strftime("%d.%m.%y") + '-' + today.strftime("%H.%M.%S")
    fh = open(DIR_PHOTOS + "\\img_" + cur_time+ ".jpg", "wb")
    fh.write(base64.b64decode(data))
    fh.close()
    return "Success"

