# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/9 15:16'

from django.conf.urls import url
from operation.views import UserAskView
urlpatterns = [
    # 用户咨询
    url('^userask/$', UserAskView.as_view(), name="userask"),
        ]