# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from .models import Course, Lesson, Video
from operation.models import UserFavorate
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class CourseListView(View):
    '''课程列表页'''
    def get(self, request):
        current = 'course_list'
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = all_courses.order_by('fav_nums')[:3]
        sort = request.GET.get('sort', '')
        if sort == 'time':
            all_courses = all_courses.order_by('-add_time')
        elif sort == 'hot':
            all_courses = all_courses.order_by('fav_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('students')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 5, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
            'current': current,
        })


class CourseDetailView(View):
    '''课程详情页'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加点击数
        course.click_num += 1
        course.save()
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        lesson = course.lesson_set.all().count()
        learn_students = course.usercourse_set.all()[:5]
        course_user_fav = False
        org_user_fav = False
        if request.user.is_authenticated:
            if UserFavorate.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_user_fav = True
            if UserFavorate.objects.filter(user=request.user, fav_id=course.id, fav_type=2):
                org_user_fav = True
        return render(request, 'course-detail.html', {
            'course': course,
            'lesson': lesson,
            'learn_students': learn_students,
            'relate_course': relate_course,
            'course_user_fav': course_user_fav,
            'org_user_fav': org_user_fav,
        })


class LessonView(View):
    '''章节信息'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = Lesson.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'lessons': lessons,
        })

