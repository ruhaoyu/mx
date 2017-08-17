# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/14 20:32'

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, LessonView
urlpatterns = [
    # 课程列表
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    # 章节信息
    url(r'^lesson/(?P<course_id>\d+)/$', LessonView.as_view(), name="course_lesson"),
        ]