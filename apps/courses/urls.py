# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/14 20:32'

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, LessonView, VidioPlayView
urlpatterns = [
    # 课程列表
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    # 课程章节详细信息
    url(r'^lesson/(?P<course_id>\d+)/$', LessonView.as_view(), name="course_lesson"),
    # 视频播放页面
    url(r'^video/(?P<video_id>\d+)/$', VidioPlayView.as_view(), name="video_play"),
        ]