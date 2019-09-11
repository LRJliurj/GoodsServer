from keras.applications.vgg19 import VGG19,preprocess_input
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
graph = tf.get_default_graph()
model_vgg19 = VGG19(weights='imagenet', include_top=False)
class Feature:
    def get_feature_by_net(self,img_file):
        global graph
        with graph.as_default():
            img = image.load_img(img_file, target_size=(224,224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            features = model_vgg19.predict(x)
            # print (features.shape)
            # print (features[0][0])
            return features

    def get_features_by_net(self,img_files):
        imgs = []
        global graph
        with graph.as_default():
            for file_path in img_files:
                img = image.load_img(file_path, target_size=(224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                # x = preprocess_input(x)
                imgs.append(x)
            x = np.concatenate([x for x in imgs])
            result = model_vgg19.predict(x)
            # print (len(result))
            # print (result[0][0].shape)
            return result

if __name__=='__main__':
    feature = Feature()
    img_files=['D:\\opt\\data\\goods\\step2_test1\\212320.931939_train_augment0.jpg','D:\\opt\\data\\goods\\step2_test1\\212331.484267_train_augment0.jpg','D:\\opt\\data\\goods\\step2_test1\\212336.257936_train_augment0.jpg']
    feature.get_features_by_net(img_files)

    img_file= 'D:\\opt\\data\\goods\\step2_test1\\212320.931939_train_augment0.jpg'
    feature.get_feature_by_net(img_file)
