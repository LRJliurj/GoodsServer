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
    test_jpg_path = "E:\\opt\\data\\1_small\\"
    test_jpg_write_path = "E:\\opt\\data\\1_small_write1\\"
    test(test_jpg_path,test_jpg_write_path)
