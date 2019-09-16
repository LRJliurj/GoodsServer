from django.shortcuts import HttpResponse
from goods.net.vgg19_net import Feature
from utils import logutil
from set_config import config
import os
from goods.util.distance_util import pdis
import numpy as np
from goods.net.kmean import Kmeans
from utils.http_out import result_failed,result_success
from goods.util.kmean_util import online_util
import subprocess
import demjson
import time
online = online_util()
feature = Feature()
kmean = Kmeans()
log = logutil.Log(cmdlevel='debug')
log_address=config.log_prams['log_path']
log.set_logger(cmdlevel='debug', log_address=log_address, modelname='ClusterGoods')
clf = kmean.load_model()
goods_cluster_train_shell = config.shell_params['goods_cluster_train_shell']
class ClusterGoods:
    def get_topn_many(self, request):
        try:
            img_local_files_ = request.POST.get('img_local_files')
            trace_id = request.POST.get('trace_id')
            img_local_files = []
            log.info(
                "trace_id = {%s},img_local_file={%s}" % (trace_id, str(img_local_files_)))
            for img_local_file in str(img_local_files_).split(","):
                if os.path.isfile(img_local_file) == False:
                    log.error(
                        "trace_id = {%s},img_local_file is not exsit,img_local_file={%s}" % (trace_id, str(img_local_file)))
                else:
                    img_local_files.append(img_local_file)
            if len(img_local_files)<1:
                log.error(
                    "trace_id = {%s},img_local_files all is not exsit,img_local_files={%s}" % (
                    trace_id, str(img_local_files)))
                return HttpResponse(str(result_failed()))
            log.info("vgg predict start time :"+str(time.time()))
            file_features = feature.get_features_by_net(img_local_files)
            # print (file_features.shape)
            f1ss = []
            for file_feature in file_features:
                # print(file_feature.shape)
                featArr = file_feature[0]
                (w, h) = featArr.shape
                featArr.resize(1, w * h)
                featArr.resize(h, w)
                # print(featArr.shape)
                f1s = []
                for f1 in featArr:
                    f1s.append(float(np.sum(f1)))
                # print("feature_img" + str(f1s))
                f1ss.append(f1s)
            log.info("kmean predict start time :" + str(time.time()))
            cluter_labels = clf.predict(f1ss)
            # print("cluter_label" + str(cluter_labels))
            ret={}
            log.info("get local file features start time :" + str(time.time()))
            for cluter_label,img_local_file,img_feature in zip(cluter_labels,img_local_files,f1ss):
                upcs = online.get_topn_upc(cluter_label, img_feature)
                ret[img_local_file] = upcs
            # log.info("trace_id = {%s},,ret={%s}" % (trace_id, str(demjson.encode(ret))))
            log.info("getmany_topn end time :" + str(time.time()))
            log.info("trace_id={%s},ret={%s}"%(trace_id,str(ret)))
            return HttpResponse(str(result_success(ret)))
        except:
            log.trace()


    def get_topn(self,request):
        try:
            img_local_file = request.POST.get('img_local_file')
            trace_id = request.POST.get('trace_id')
            if os.path.isfile(img_local_file) == False:
                log.info("trace_id = {%s},img_local_file is not exsit,img_local_file={%s}"%(trace_id,str(img_local_file)))
                return HttpResponse(str(result_failed()))
            file_features = feature.get_feature_by_net(img_local_file)
            # print (file_features)
            featArr = file_features[0][0]
            (w, h) = featArr.shape
            featArr.resize(1, w * h)
            featArr.resize(h, w)
            # print(featArr.shape)
            f1s = []
            for f1 in featArr:
                f1s.append(float(np.sum(f1)))
            # print ("feature_img"+str(f1s))
            cluter_label = clf.predict([f1s])[0]
            # print("cluter_label" + str(cluter_label))
            # to_cluter_dis = pdis(f1s,clf.cluster_centers_[cluter_label])[0]
            upcs = online.get_topn_upc(cluter_label,f1s)
            log.info("trace_id = {%s},img_local_file={%s},upcs={%s},cluter_label={%s}"%(trace_id,img_local_file,str(upcs),str(cluter_label)))
            data = {"upcs":upcs}
            return HttpResponse(str(result_success(data)))
        except:
            log.trace()

    def add_good_img(self,request):
        try:
            img_local_file = request.POST.get('img_local_file')
            goods_shelfgoods_id = request.POST.get('goods_shelfgoods_id')
            good_upc = request.POST.get('good_upc')
            trace_id = request.POST.get('trace_id')
            log.info("trace_id = {%s},img_local_file={%s},goods_shelfgoods_id={%s}" % (
            str(trace_id), str(img_local_file), str(goods_shelfgoods_id)))
            if os.path.isfile(img_local_file) == False:
                log.error("trace_id = {%s},img_local_file is not exsit,img_local_file={%s},goods_shelfgoods_id={%s}" % (str(trace_id),str(img_local_file),str(goods_shelfgoods_id)))
                return HttpResponse(str(result_failed()))
            file_features = feature.get_feature_by_net(img_local_file)
            featArr = file_features[0][0]
            (w, h) = featArr.shape
            featArr.resize(1, w * h)
            featArr.resize(h, w)
            print(featArr.shape)
            f1s = []
            for f1 in featArr:
                f1s.append(float(np.sum(f1)))
            cluter_label = clf.predict([f1s])[0]
            to_cluter_dis = pdis(f1s,clf.cluster_centers_[cluter_label])[0]
            # filename = os.path.basename(os.path.realpath(img_local_file))
            # online.save_new_goods_feature(cluter_label, to_cluter_dis, good_upc, f1s, filename)
            online.save_new_goods_feature(cluter_label,to_cluter_dis,good_upc,f1s,goods_shelfgoods_id)
            log.info("trace_id={%s},img_local_file={%s},add_good_img sucess,cluter_label={%s}" % (str(trace_id),img_local_file,str(cluter_label)))
            data = ''
            return HttpResponse(str(result_success(data)))
        except:
            log.trace()
    def delete_good_img(self,request):
        try:
            goods_shelfgoods_id= request.POST.get('goods_shelfgoods_id')
            trace_id = request.POST.get('trace_id')
            log.info("trace_id = {%s},goods_shelfgoods_id={%s}" % (
                str(trace_id),str(goods_shelfgoods_id)))
            code = online.delete_feature(goods_shelfgoods_id)
            if code == 0 :
                data = ''
                log.info("trace_id = {%s},goods_shelfgoods_id={%s},delete success" % (
                    str(trace_id), str(goods_shelfgoods_id)))
                return HttpResponse(str(result_success(data)))
            else :
                log.info("trace_id = {%s},goods_shelfgoods_id={%s},delete failed" % (
                    str(trace_id), str(goods_shelfgoods_id)))
                return HttpResponse(str(result_failed()))
        except:
            log.trace()
    def train_cluter_good(self,request):
        try:
            trace_id = request.POST.get('trace_id')
            #os.popen(goods_cluster_train_shell)
            return_code = subprocess.call(goods_cluster_train_shell, shell=True)
            log.info("trace_id={%s},train_cluter_good sucess,return_code=" % (str(trace_id),str(return_code)))
            data = ''
            return HttpResponse(str(result_success(data)))
        except:
            log.trace()




