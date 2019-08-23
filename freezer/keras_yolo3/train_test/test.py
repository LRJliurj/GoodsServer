from freezer.keras_yolo3.yolo3 import yolo
import os
from PIL import Image
import cv2
YOLO = yolo.YOLO()

def test(test_jpg_path,test_jpg_write_path):
    files = os.listdir(test_jpg_path)
    for file in files:
        img = Image.open(os.path.join(test_jpg_path,file))
        img = YOLO.detect_image(img)
        img.save(os.path.join(test_jpg_write_path,file))

if __name__=='__main__':
    test_jpg_path = "E:\\opt\\online_data\\20190821_09\\"
    test_jpg_write_path = "E:\\opt\\online_data\\test_write\\"
    test(test_jpg_path,test_jpg_write_path)
