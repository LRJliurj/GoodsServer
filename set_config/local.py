yolov3_predict={
        "good_model_path": '/home/ai/ai_code/keras-yolov3-master/model_data/yolo.h5',
        "anchors_path": '/home/ai/ai_code/keras-yolov3-master/model_data/yolo_anchors.txt',
        "classes_path": '/home/ai/ai_code/keras-yolov3-master/model_data/voc_classes.txt',
        "score" : 0.2,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 1,
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