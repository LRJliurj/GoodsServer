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
online = online_util()
feature = Feature()
kmean = Kmeans()
log = logutil.Log(cmdlevel='debug')
log_address=config.log_prams['log_path']
log.set_logger(cmdlevel='debug', log_address=log_address, modelname='ClusterGoods')
clf = kmean.load_model()
goods_cluster_train_shell = config.shell_params['goods_cluster_train_shell']
class ClusterGoods:
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
            print(featArr.shape)
            f1s = []
            for f1 in featArr:
                f1s.append(float(np.sum(f1)))
            print ("feature_img"+str(f1s))
            cluter_label = clf.predict([f1s])[0]
            print("cluter_label" + str(cluter_label))
            to_cluter_dis = pdis(f1s,clf.cluster_centers_[cluter_label])[0]
            upcs = online.get_topn_upc(cluter_label,to_cluter_dis)
            log.info("trace_id = {%s},img_local_file={%s},upcs={%s}"%(trace_id,img_local_file,str(upcs)))
            data = {"upcs":upcs}
            return HttpResponse(str(result_success(data)))
        except:
            log.trace()

    def add_good_img(self,request):
        try:
            img_local_file = request.POST.get('img_local_file')
            good_upc = request.POST.get('good_upc')
            trace_id = request.POST.get('trace_id')
            if os.path.isfile(img_local_file) == False:
                log.info("trace_id = {%s},img_local_file is not exsit,img_local_file={%s}" % (str(trace_id),str(img_local_file)))
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
            print (cluter_label)
            to_cluter_dis = pdis(f1s,clf.cluster_centers_[cluter_label])[0]
            print (to_cluter_dis)
            filename = os.path.basename(os.path.realpath(img_local_file))
            online.save_new_goods_feature(cluter_label,to_cluter_dis,good_upc,f1s,filename)
            log.info("trace_id={%s},img_local_file={%s},add_good_img sucess,cluter_label={%s}" % (str(trace_id),img_local_file,str(cluter_label)))
            data = ''
            return HttpResponse(str(result_success(data)))
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




