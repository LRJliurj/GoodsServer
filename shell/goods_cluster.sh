#!/bin/bash
# 重新训练聚类模型的脚本
pid=`ps -ef | grep goods_cluster | awk 'BEGIN{FS=" "}{print $2}'`
kill -9 $pid
cd ../
python3 train_cluster_alter.py