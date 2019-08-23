"""GoodsServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from goods.service import cluster_goods
clustergoods = cluster_goods.ClusterGoods()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_goods_topn',clustergoods.get_topn),
    path('api/add_new_good',clustergoods.add_good_img),
    path('api/train_cluster_goods',clustergoods.train_cluter_good)
]
