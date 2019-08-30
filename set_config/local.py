freezer_params={
    "yolov3_predict":{
        "good_model_path": 'E:\\opt\\model\\yolo3_freezer\\ep3587-loss46.704-val_loss52.474.h5',
        "anchors_path": 'E:\\opt\\code\\github\\GoodsServer\\freezer\\keras_yolo3\\model_data\\yolo_anchors.txt',
        "classes_path": 'E:\\opt\\code\\github\\GoodsServer\\freezer\\keras_yolo3\\model_data\\voc_classes.txt',
        "score" : 0.1,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 0,
        "font_file":'E:\\opt\\code\\github\\GoodsServer\\freezer\\keras_yolo3\\font\\FiraMono-Medium.otf',
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
        "n_cluters":40,
        "top_n":50,
        "batch_size":200,
        "model_file":"E:\\opt\\model\\kmean_goods\\goods.pkl",
        "online":{
            #kmean 聚类后带聚里的特征数据
            "kmean_predict_features_path":"E:\\opt\\data\\kmean_predict\\"
        },
        "offline":{
            #kmean 聚类前 vgg19预测的特征数据
            "vgg_predict_features_path":"E:\\opt\\data\\step2_all_feature\\"
        },
    },
    "vgg19_params":{
        "model_file":"C:\\Users\\admin\\.keras\\models\\vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5",
        "online":{
            "goods_dir_path":"E:\\opt\\data\\goods_path\\",
        },
        "offline":{
            "goods_dir_path": "E:\\opt\\data\\step2_all\\step2\\",
        }
    }
}

linear_params={
    "num_iter_first":10000,
    "step_size":1.0,
    "mini_batch_frction":1.0,
    "num_iter_alter": 50,
}


shellgoods_params={
    "spark_context":"spark://192.168.1.60:7077",
}

db_context={
    "url":"jdbc:mysql://192.168.1.52:3306/dmstore",
    "driver":"com.mysql.jdbc.Driver",
    "user":"work",
    "password":"UQrwsfpVZ12pvv24",
}


log_prams = {
    "log_path":"E:\\opt\\logs\\"
}

shell_params={
    'goods_cluster_train_shell':"sh ./shell/goods_cluster.sh"
}


