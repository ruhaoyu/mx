# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/7/31 16:04'
import xadmin
from .models import Course, Lesson, Video, CourseRecourse

class CourseAdmin(object):
    list_display = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time')
    search_fields = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num')
    list_filter = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time')


class LessonAdmin(object):
    list_display = ('course', 'name', 'add_time')
    search_fields = ('course', 'name')
    list_filter = ('course__name', 'name', 'add_time')


class VideoAdmin(object):
    list_display = ('lesson', 'name', 'add_time')
    search_fields = ('lesson', 'name')
    list_filter = ('lesson', 'name', 'add_time')


class CourseRecourseAdmin(object):
    list_display = ('course', 'name', 'download', 'add_time')
    search_fields = ('course', 'name', 'download')
    list_filter = ('course', 'name', 'download', 'add_time')

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseRecourse, CourseRecourseAdmin)