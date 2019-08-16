__author__ = 'admin'
# *_*coding:utf-8 *_*
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_v3 import InceptionV3
from keras.applications.nasnet import NASNetLarge,preprocess_input
from keras.preprocessing import image
import numpy as np

model_vgg16 = VGG16(weights='imagenet', include_top=False)
model_vgg19 = VGG19(weights='imagenet', include_top=False)
model_resnetv2 = InceptionResNetV2(weights='imagenet', include_top=False)
model_inceptionv3 = InceptionV3(weights='imagenet', include_top=False)
model_nasnet=NASNetLarge(weights='imagenet', include_top=False)

models = {
    "vgg16":model_vgg16,
    "vgg19":model_vgg19,
    "resnetv2":model_resnetv2,
    "inceptionv3":model_inceptionv3,
    "nasnet":model_nasnet
}

model_size ={
    "vgg16":(224,224),
    "vgg19":(224,224),
    "resnetv2":(224,224),
    "inceptionv3":(224,224),
    "nasnet":(331,331)
}

class Feature:
    def get_feature_by_net(self,net_name,img_file):
        img = image.load_img(img_file, target_size=model_size[net_name])
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = models[net_name].predict(x)
        return features



