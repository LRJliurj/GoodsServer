yolov3_predict={
        "good_model_path": 'E:\\opt\\model\\yolo3_freezer\\ep3587-loss46.704-val_loss52.474.h5',
        "anchors_path": 'E:\\opt\\code\\github\\GoodsServer\\freezer\\keras_yolo3\\model_data\\yolo_anchors.txt',
        "classes_path": 'E:\\opt\\code\\github\\GoodsServer\\freezer\\keras_yolo3\\model_data\\voc_classes.txt',
        "score" : 0.05,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 0,
        "font_file":'E:\\opt\\code\\github\\GoodsServer\\freezer\\keras_yolo3\\font\\FiraMono-Medium.otf'
}

yolov3_train_params = {
    'annotation_path' : '/home/ai/code/keras-yolov3/train_data/2007_train.txt',
    'log_dir' : '/home/ai/code/keras-yolov3/logs/000/',
    'classes_path' : '/home/ai/code/keras-yolov3/model_data/voc_classes.txt',
    'anchors_path' : '/home/ai/code/keras-yolov3/model_data/yolo_anchors.txt',
    'out_name' : 'yolov3_trained_weights.h5',
    #'weight_path' : '/opt/ai_code/keras-yolov3-master/model_data/yolov3_weights.h5',
    'weight_path' : '/home/ai/code/keras-yolov3/model_data/ep103-loss30.705-val_loss28.950.h5',
    'batch_size': 10,
    'epochs' : 500,
    'initial_epoch' : 103,
    'period': 1,
    "val_split":0.3
}