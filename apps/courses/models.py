# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'机构', null=True, blank=True, on_delete=models.SET_NULL)
    course_teacher = models.ForeignKey(Teacher, verbose_name=u'课程教师', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    dsc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情	', width=600, height=300, imagePath="course/ueditor",
                          filePath="course/ueditor", default='')
    youneed_know = models.CharField(max_length=200, default='', verbose_name=u'课程须知')
    teacher_tell = models.CharField(max_length=200, default='', verbose_name=u'老师告诉你')
    course_notice = models.CharField(max_length=50, verbose_name=u'课程公告', null=True, blank=True)
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=5, verbose_name=u'难度等级')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name=u'课程类别')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u'封面', max_length=100)
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    tag = models.CharField(default="", verbose_name=u'课程标签', max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='www.baidu.com'>跳转</a>")

    go_to.short_description = '跳转'

    def get_learn_students(self):
        # 获取学习用户数量
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_video_name(self):
        '''获取课程信息名称'''
        return self.video_set.all()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    video_times = models.IntegerField(default=0, verbose_name=u'视频时长（分钟数）')
    url = models.CharField(max_length=200, default='', verbose_name=u'访问地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class CourseRecourse(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
