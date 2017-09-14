# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/9 15:16'

from django.conf.urls import url
from operation.views import UserAskView
from .views import CourseCommentView, AddCommentView
urlpatterns = [
    # 用户咨询
    url('^userask/$', UserAskView.as_view(), name="userask"),
    # 课程评论
    url('^course_comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    # 添加课程评论
    url('^add_comment/$', AddCommentView.as_view(), name='add_comment'),
        ]