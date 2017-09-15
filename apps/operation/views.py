# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .forms import UserAskForm
from .models import CourseComment, Course, UserCourse
from courses.models import CourseRecourse
from django.views.generic.base import View
from utils.mixin_urils import LoginRequiredMixin


# 用户咨询
class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save()
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse('{"status":"fail", "msg": "添加出错"}')


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        comments = CourseComment.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course=course)
        # 取出该课程的所有用户id
        users = [user_course.user for user_course in user_courses]
        # 通过用户id列表，取出所有课程
        all_course = UserCourse.objects.filter(user__in=users)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        course_resourse = CourseRecourse.objects.filter(course=course)
        return render(request, 'course-comment.html',{
               'course': course,
            'comments': comments,
            'relate_courses': relate_courses,
            'course_resourse': course_resourse,
        })


class AddCommentView(View):
    '''用户添加课程评论'''
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', 0)
        if course_id > 0 and comments:
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.user = request.user
            course_comment.comment = comments
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}')
