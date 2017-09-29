# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/7/31 16:04'
import xadmin
from .models import Course, Lesson, Video, CourseRecourse, BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time', 'get_zj_nums', 'go_to')
    search_fields = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num')
    list_filter = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time')
    ordering = ['-click_num']
    # 一次性拉取数据改成输入时候匹配搜索
    relfield_style = 'fk-ajax'
    # 只读字段设置
    readonly_fields = ['click_num']
    # 在列表页可以编辑
    list_editable = ['degree', 'desc']
    # 不显示某些字段
    exclude = ['fav_nums']
    # 添加课程的时候，可以添加章节
    inlines = [LessonInline]
    # 定时刷新
    refresh_times = [3,5]
    style_fields = {'detail': 'ueditor'}

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        query_set = qs.filter(is_banner = False)
        return query_set


class BannerCourseAdmin(object):
    list_display = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time')
    search_fields = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num')
    list_filter = ('name', 'dsc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time')
    ordering = ['-click_num']
    relfield_style = 'fk-ajax'
    readonly_fields = ['click_num']
    list_editable = ['degree', 'desc']
    exclude = ['fav_nums']
    inlines = [LessonInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        query_set = qs.filter(is_banner = True)
        return query_set


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseRecourse, CourseRecourseAdmin)