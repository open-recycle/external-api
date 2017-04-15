#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import serial
import os
import argparse
import json

SERIAL_PORT = '/dev/ttyACM0'
_URL_API_ = "http://217.71.231.9:48777/api/UploadFile4Recognition"
USER_ID = ""
IMAGE_TYPE = ""
IM_PATH = "C:\\Users\\Starforge\\PycharmProjects\\ML\\img\\230120868_65719_11184317241402216442.jpg"
# IM_PATH = '/mnt/sda1/pic.jpg'


def upload_to_web(im_path):
    global _URL_API_, USER_ID, IMAGE_TYPE
    try:
        fileData = open(im_path, "rb").read()
        files = {'file': (open(im_path,'rb'), fileData, {'Expires': '0'})}

        data = {'user_id': USER_ID,
                'filename': IMAGE_TYPE}

        # print "\n\nfiles:", files, "\n\ndata:", data, "\n\n"
        req = requests.put(url=_URL_API_, files=files, data=data)
        # print "\n\nRequest:", req, "\n\nReqTEXT", req.text, "ReqContent", req.content

        print u"\n\n***ПОЛУЧЕН ОТВЕТ***\n", req.text

        json_string = json.loads(req.text, encoding="utf-8")
        recycle_type = json_string.get('Message') # <-- это распознанный тип

        print u"\n\n***РАСПОЗНАН ОТВЕТ***\n", recycle_type, "\n"
        # TODO добавить преобразование типа в код, для отправки в YUN
        if recycle_type == u"пластиковая бутылка" :
            return 0
        elif recycle_type == u"стеклянная бутылка" :
            return 1
        # TODO ...и т.д.

    except Exception as ex:
        print u"\n\n***EXCEPTION***\n", ex
        return None

def send_data_to_serial(data):
    print(u'***ОТПРАВКА РЕЗУЛЬТАТА В ПОРТ YUN***')
    global SERIAL_PORT
    try:
        ser = serial.Serial(SERIAL_PORT, 9600)
        if SERIAL_PORT.isOpen():
            if(ser.write(data)):
                return True
            else:
                return False
    except Exception as ex:
        print(ex)
        return False

def init():
    # задаются параметры приложения
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i",
        "--image",
        type=str,
        required=True,
        help=u"Директория поиска изображений"
    )
    ap.add_argument(
        "-a",
        "--angle",
        type=int,
        required=False,
        default=2,
        help=u"Угол поворота изображения (по-умолчанию: 2 градуса)"
    )
    return vars(ap.parse_args())

if __name__ == "__main__":
    IM_PATH
    print(u"\n***АНАЛИЗ ПАРАМЕТРОВ***")
    args = init()
    # получение значения параметра "Директория поиска изображений"
    input_directory = args["image"]
    # получение значения параметра "Угол поворота"
    angle = args["angle"]
    IM_PATH = input_directory
    
    try:
        file = open(IM_PATH)
    except IOError as e:
        print(u'Image not found at path: ', IM_PATH)
    else:
        with file:
            print(u'***ОТПРАВКА ИЗОБРАЖЕНИЯ НА СЕРВЕР***')
            if(send_data_to_serial(upload_to_web(IM_PATH))):
                print("complete")
            else:
                print("failed")
