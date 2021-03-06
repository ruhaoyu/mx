# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models


# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(default='pxjg', max_length=20, choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高效')),
                                verbose_name=u'机构类别')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数量')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数量')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'封面图')
    address = models.CharField(max_length=150, verbose_name=u'地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市', on_delete=models.SET_NULL, null=True)
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_num = models.IntegerField(default=0, verbose_name=u'课程数量')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    # 获取教师数
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    # 获取课程数
    def get_course_num(self):
        return self.course_set.all().count()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, verbose_name=u'教师名称')
    age = models.IntegerField(verbose_name=u'教师年龄', default=0)
    work_year = models.IntegerField(default=0, verbose_name=u'工作年限')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'教师头像', null=True, blank=True)
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数量')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数量')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    # 获取课程数
    def get_course_num(self):
        return self.course_set.all().count()

    # 获取课程
    def get_course(self):
        return self.course_set.all()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
