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
feature = Feature()
kmean = Kmeans()
log = logutil.Log(cmdlevel='debug')
log_address=config.log_prams['log_path']
log.set_logger(cmdlevel='debug', log_address=log_address, modelname='ClusterGoods')
kmean_model_file = config.goods_params['kmean_params']['model_file']
clf = kmean.load_model(kmean_model_file)
goods_cluster_train_shell = config.shell_params['goods_cluster_train_shell']
class ClusterGoods:
    def get_topn(self,request):
        try:
            img_local_file = request.POST.get('img_local_file')
            if os.path.isfile(img_local_file) == False:
                log.info("img_local_file is not exsit,img_local_file={%s}"%(str(img_local_file)))
                return HttpResponse(str(result_failed()))
            file_features = feature.get_feature_by_net(img_local_file)
            featArr = file_features[0][0]
            f1s = []
            for f1 in featArr:
                f1s.append(np.sum(f1))
            print ("feature_img"+str(len(f1s)))
            cluter_label = clf.predict(f1s)
            upcs = online_util.get_topn_upc(cluter_label)
            log.info("img_local_file={%s},upcs={%s}"%(img_local_file,str(upcs)))
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
            f1s = []
            for f1 in featArr:
                f1s.append(np.sum(f1))
            print("feature_img" + str(len(f1s)))
            cluter_label = clf.predict(f1s)
            to_cluter_dis = pdis(f1s,clf.cluster_centers_[cluter_label])
            filename = os.path.basename(os.path.realpath(img_local_file))
            online_util.save_new_goods_feature(cluter_label,to_cluter_dis,good_upc,f1s,filename)
            log.info("trace_id={%s},img_local_file={%s},add_good_img sucess" % (str(trace_id),img_local_file))
            data = ''
            return HttpResponse(str(result_success(data)))
        except:
            log.trace()

    def train_cluter_good(self,request):
        try:
            trace_id = request.POST.get('trace_id')
            os.popen(goods_cluster_train_shell)
            log.info("trace_id={%s},train_cluter_good sucess" % (str(trace_id)))
            data = ''
            return HttpResponse(str(result_success(data)))
        except:
            log.trace()




