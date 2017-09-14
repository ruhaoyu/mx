# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .forms import UserAskForm
from .models import CourseComment, Course
from django.views.generic.base import View


# 用户咨询
class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save()
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse('{"status":"fail", "msg": "添加出错"}')


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        comments = CourseComment.objects.filter(course=course)
        return render(request, 'course-comment.html',{
               'course': course,
            'comments': comments,
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
