# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/9 12:24'


from django.conf.urls import url
from organization.views import OrgView
urlpatterns = [
    # 课程机构首页
    url('^list/$', OrgView.as_view(), name="org_list"),
        ]