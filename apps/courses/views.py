# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from .models import Course, Lesson, Video, CourseRecourse
from operation.models import UserFavorate, UserCourse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_urils import LoginRequiredMixin
from django.db.models import Q
# Create your views here.

class CourseListView(View):
    '''课程列表页'''
    def get(self, request):
        current = 'course_list'
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = all_courses.order_by('-fav_nums')[:3]
        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(detail__icontains=search_keywords)|Q(dsc__icontains=search_keywords))
        sort = request.GET.get('sort', '')
        if sort == 'time':
            all_courses = all_courses.order_by('-add_time')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-fav_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')
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
            relate_course = Course.objects.filter(tag=tag).exclude(id=course.id)[:3]
        else:
            relate_course = []
        # lesson = course.lesson_set.all().count()
        learn_students = course.usercourse_set.all()[:5]
        course_user_fav = False
        org_user_fav = False
        if request.user.is_active:
            if UserFavorate.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_user_fav = True
            if UserFavorate.objects.filter(user=request.user, fav_id=course.id, fav_type=2):
                org_user_fav = True
        return render(request, 'course-detail.html', {
            'course': course,
            'learn_students': learn_students,
            'relate_course': relate_course,
            'course_user_fav': course_user_fav,
            'org_user_fav': org_user_fav,
        })


class LessonView(LoginRequiredMixin,View):
    '''章节信息'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = Lesson.objects.filter(course=course)
        course.students += 1
        course.save()
        # 判断用户是否关联该用户
        user = UserCourse.objects.filter(user=request.user, course=course)
        if not user:
            user_course = UserCourse()
            user_course.course = course
            user_course.user = request.user
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        # 取出该课程的所有用户id
        users = [user_course.user for user_course in user_courses]
        # 通过用户id列表，取出所有课程
        all_course = UserCourse.objects.filter(user__in=users)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_course]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        course_resourse = CourseRecourse.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'lessons': lessons,
            'course_resourse': course_resourse,
            'relate_courses': relate_courses,
        })


class VidioPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course
        lesson = video.lesson
        user_courses = UserCourse.objects.filter(course=course)
        # 取出该课程的所有用户id
        users = [user_course.user for user_course in user_courses]
        # 通过用户id列表，取出所有课程
        all_course = UserCourse.objects.filter(user__in=users)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_course]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        course_resourse = CourseRecourse.objects.filter(course=course)
        return render(request, 'video_play.html',{
            'video': video,
            'course': course,
            'lesson': lesson,
            'relate_courses': relate_courses,
            'course_resourse': course_resourse,
        })


