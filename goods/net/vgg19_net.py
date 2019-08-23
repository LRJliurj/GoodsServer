from keras.applications.vgg19 import VGG19,preprocess_input
from keras.preprocessing import image
import numpy as np
model_vgg19 = VGG19(weights='imagenet', include_top=False)
class Feature:
    def get_feature_by_net(self,img_file):
        img = image.load_img(img_file, target_size=(224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model_vgg19.predict(x)
        return features