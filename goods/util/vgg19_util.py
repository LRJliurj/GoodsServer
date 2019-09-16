import os
from goods.net.vgg19_net import Feature
from set_config import config
goods_dir_path = config.goods_params['vgg19_params']['offline']['goods_dir_path']
vgg_predict_features_path = config.goods_params['kmean_params']['offline']['vgg_predict_features_path']
feature = Feature()
vgg_predict_features_path1 = config.goods_params['kmean_params']['offline']['vgg_predict_features_path1']
# 测试 对400个品（step2） 做预测
def predict ():
    for goods_path in os.listdir(goods_dir_path):
        good_path = os.path.join(goods_dir_path,goods_path)
        vgg_predict_file = os.path.join(vgg_predict_features_path,str(goods_path)+".txt")
        with open(vgg_predict_file, "w") as f:
            for img_file in os.listdir(good_path):
                img_file_path = os.path.join(good_path,img_file)
                feat = feature.get_feature_by_net(img_file_path)
                featArr = feat[0][0]
                (w,h) = featArr.shape
                featArr.resize(1,w*h)
                ft = ''
                ft = ft +img_file
                for fe in featArr[0]:
                     ft  = ft + "," + str(fe)
                f.write(ft)
                f.write("\n")

# 线上对15000个图片做预测

# 测试 对400个品（step2） 做预测
def predict_features ():
        with open(vgg_predict_features_path1, "w") as f:
            for img_file in os.listdir(goods_dir_path):
                img_file_path = os.path.join(goods_dir_path,img_file)
                feat = feature.get_feature_by_net(img_file_path)
                featArr = feat[0][0]
                (w,h) = featArr.shape
                featArr.resize(1,w*h)
                ft = ''
                ft = ft +img_file
                for fe in featArr[0]:
                     ft  = ft + "," + str(fe)
                f.write(ft)
                f.write("\n")
