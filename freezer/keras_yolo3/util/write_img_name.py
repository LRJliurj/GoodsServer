from sklearn.model_selection import train_test_split
import os
from random import shuffle
filenames=[]
files=os.listdir('/home/ai/ai_data/yolov3/VOCdevkit/VOC2007/JPEGImages/')
for filename in files:
   filenames.append(str(filename).split('.')[0])
shuffle(filenames)
#train,val=train_test_split(filenames,test_size=0.5)

with open("/home/ai/ai_data/yolov3/VOCdevkit/VOC2007/ImageSets/Main/train.txt",'w') as f:
   for tr in filenames:
      f.write(tr)
      f.write("\n")

#with open("/home/ai/ai_data/yolov3/VOCdevkit/VOC2007/ImageSets/Main/val.txt",'w') as f:
#   for v in val:
#      f.write(v)
#      f.write("\n")