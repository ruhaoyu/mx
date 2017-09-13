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
        return render(request, 'course-comment.html',{
               'course': course,
        })