freezer_params={
    "yolov3_predict":{
        "good_model_path": '/home/ai/model/freezer/ep3587-loss46.704-val_loss52.474.h5',
        "anchors_path": './freezer/keras_yolo3/model_data/yolo_anchors.txt',
        "classes_path": './freezer/keras_yolo3/model_data/voc_classes.txt',
        "score" : 0.1,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 0,
        "font_file":'./freezer/keras_yolo3/font/FiraMono-Medium.otf',
        "diff_switch_iou":(True,0.6),
        "single_switch_iou_minscore":(True,0.0,0.3)
    },
    "yolov3_train_params" : {
    'annotation_path' : '/home/ai/code/keras-yolov3/train_data/2007_train.txt',
    'log_dir' : '/home/ai/code/keras-yolov3/logs/000/',
    'classes_path' : '/home/ai/code/keras-yolov3/model_data/voc_classes.txt',
    'anchors_path' : '/home/ai/code/keras-yolov3/model_data/yolo_anchors.txt',
    'out_name' : 'yolov3_trained_weights.h5',
    'weight_path' : '/home/ai/code/model/',
    'batch_size': 10,
    'epochs' : 500,
    'initial_epoch' : 103,
    'period': 1,
    "val_split":0.3
    }
}
goods_params = {

    "kmean_params" : {
        "n_cluters":200,
        "top_n":50,
        "batch_size":100,
        "model_file":"/home/ai/model/cluster_goods/goods.pkl",
        "online":{
            #kmean 聚类后带排序的特征数据
            "kmean_predict_features_path":"/home/ai/data/feature_data/cluster_goods/"
        },
        "offline":{
            #kmean 聚类前 vgg19预测的特征数据
            "vgg_predict_features_path":"/home/ai/data/feature_data/class_goods/",
            "vgg_predict_features_path1":"/home/ai/data/feature_data/class_goods/vgg_features.txt"
        },
    },
    "vgg19_params":{
        "model_file":"~/.keras/models/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5",
        "online":{
            #线上聚类接口传入时，图片的默认本地路径
            "goods_dir_path":"/home/ai/data/goods/",
        },
        "offline":{
            #离线预测时，400类别的图片路径目录
            "goods_dir_path": "/home/ai/data/step2/",
        }
    }
}


shellgoods_params={
    "spark_context":"spark://192.168.1.60:7077",
    "online_model_name":"linear",
    "regressor_model_path" : {
        "linear": "/home/ai/model/regressor/LinearRegressionModel",
        "decision_tree": "/home/ai/model/regressor/DecisionTreeRegressionModel",
        "gb_tree": "/home/ai/model/regressor/GBTRegressionModel",
        "random_forest": "/home/ai/model/regressor/RandomForestRegressionModel"
    }
}

# db_context={
# #     "host":"192.168.1.52",
# #     "port":3306,
# #     "database":"dmstore",
# #     "url":"jdbc:mysql://192.168.1.52:3306/dmstore",
# #     "driver":"com.mysql.jdbc.Driver",
# #     "user":"work",
# #     "password":"UQrwsfpVZ12pvv24",
# # }
db_context={
    "host":"192.168.1.62",
    "port":3306,
    "database":"goodsdl",
    "url":"jdbc:mysql://192.168.1.62:3306/goodsdl",
    "driver":"com.mysql.jdbc.Driver",
    "user":"root",
    "password":"iShehui",
}

log_prams = {
    "log_path":"logs/"
}

shell_params={
    'goods_cluster_train_shell':"sh shell/goods_cluster.sh"
}


