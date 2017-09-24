# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from .models import UserProfile, EmailVerifyRecord
from operation.models import UserCourse, UserFavorate
from organization.models import CourseOrg, Teacher
from courses.models import Course
from operation.models import UserMessage
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ResetFrom, UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_urils import LoginRequiredMixin
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json

# Create your views here.


class CustomBackend(ModelBackend):
    '''重新定义认证，使邮箱也可以登录'''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    '''注册'''
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # email = request.POST.get("email", "")
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            search_user = UserProfile.objects.filter(email=user_name)
            # 判断用户是否存在，否则不能注册
            if not search_user:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.password = make_password(pass_word)
                user_profile.is_active = False
                user_profile.save()
                send_staute = send_register_email(user_name, "register")
                return render(request, 'login.html', {'msg': '注册成功，请激活后登录！'})
            else:
                return render(request, 'login.html', {'msg': '用户已经存在，请直接登录！'})
        else:
            return render(request, 'register.html',{'register_form': register_form})


class ActiveUserView(View):
    '''激活'''
    def get(self, request, active_code):
        email_code = EmailVerifyRecord.objects.get(code=active_code)
        email = email_code.email
        user_profile = UserProfile.objects.get(username=email)
        # 激活时判断url是否存在
        if email_code:
            user_profile.is_active = True
            user_profile.save()
        return render(request, "login.html")


class LoginView(View):
    '''登录'''
    def get(self, request):
        login_form = LoginForm()
        return render(request, "login.html", {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            try:
                user_profile = UserProfile.objects.get(username=user_name)
                user_active = user_profile.is_active
            except:
                user_profile = None
            # 判断用户是否存在，否则直接跳转登录
            if not user_profile:
                return render(request, "register.html", {'msg': '用户不存在，请先注册！'})
            # 判断用户是否激活，否则不能登录
            if user_active is True:
                user = authenticate(username=user_name, password=pass_word)
                if user is not None:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {'login_form': login_form, 'msg': '用户名或密码错误！'})
            else:
                return render(request, 'login.html', {'login_form': login_form,'msg': '用户未激活，请激活后再重新登录！'})
        else:
            return render(request, "login.html", {'login_form': login_form})



class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        logout(request)
        return render(request, 'login.html')


# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {'msg': '用户名或密码错误！'})
#     else:
#         return render(request, "login.html")


class ForgetPasswordView(View):
    '''找回密码'''
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            user_profile = UserProfile()
            user_data = UserProfile.objects.filter(username=email)
            # 判断用户是否存在
            if user_data:
                send_register_email(email, "forget")
                return render(request, 'forget_email_succese.html')
            else:
                return render(request, "forgetpwd.html", {'forget_form': forget_form, 'msg': '用户不存在！'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    '''重置密码'''
    def get(self, request, reset_code):
        reset_form = ResetFrom()
        all_recode = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_recode:
            cord_statue = EmailVerifyRecord.objects.get(code=reset_code)
            statue = cord_statue.is_used
            if not statue:
                for recode in all_recode:
                    email = recode.email
                return render(request, "reset.html", {'all_record': all_recode, 'statue': statue, 'email': email})
            else:
                return render(request, "reset.html", {'all_record': all_recode, 'statue': statue, 'msg': '链接已失效，请重新获取！'})
        else:
            # return render(request, 'resetfail.html')
            return render(request, "reset.html", {'all_record': all_recode,'msg': '用户不存在，请确认重置密码链接是否正确！'})


class ModifyView(View):
    '''修改密码，和get分开'''
    def post(self, request):
        reset_form = ResetFrom(request.POST)
        user_email = request.POST.get('email', "")
        if reset_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return render(request, 'reset.html', {'msg': '两次密码输入不一致！'})
            else:
                user_profile = UserProfile.objects.get(email=user_email)
                user_profile.password = make_password(password1)
                user_profile.save()
                verifies = EmailVerifyRecord.objects.filter(email=user_email)
                for verify in verifies:
                    last_verify = verify
                verify.is_used = True
                verify.save()
                return render(request, 'login.html', {'msg': '修改密码成功，请登录！'})
        else:
            return render(request, 'reset.html', {'reset_form': reset_form, 'email': user_email})


class UsercenterInfoView(LoginRequiredMixin, View):
    '''个人用户中心'''
    def get(self, request):
        current = 'userinfo'
        user = UserProfile.objects.get(username=request.user)
        unread_message_num = UserMessage.objects.filter(user=int(request.user.id), has_read=False).count()
        return render(request, 'usercenter-info.html', {
            'user': user,
            'current': current,
            'unread_message_num': unread_message_num,
        })


class ChangeUserImageView(LoginRequiredMixin, View):
    '''修改头像'''
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse('{"status":"fail"}')


class ChangeUserMessageView(View):
    '''修改基本资料'''
    def get(self, request):
        user = request.user
        '''获取前端填写数据并保存'''

        if request.GET.get('nick_name', ''):
            nick_name = request.GET.get('nick_name', '')
        else:
            nick_name = request.user.nick_name
        if request.GET.get('birday', ''):
            birday = request.GET.get('birday', '')
        else:
            birday = request.user.birday
        if request.GET.get('gender', ''):
            gender = request.GET.get('gender', '')
        else:
            gender = request.user.gender
        if request.GET.get('address', ''):
            address = request.GET.get('address', '')
        else:
            address = request.user.address
        if request.GET.get('mobile', ''):
            mobile = request.GET.get('mobile', '')
        else:
            mobile = request.user.mobile
        user.nick_name = nick_name
        user.birday = birday
        user.gender = gender
        user.address = address
        user.mobile = mobile
        if user.save():
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse('{"status":"fail"}')


class ModifyUserView(View):
    '''修改个人中心密码'''
    def post(self, request):
        reset_form = ResetFrom(request.POST)
        if reset_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return HttpResponse('{"status":"fail", "msg": "密码不一致"}')
            user = request.user
            user.password = make_password(password2)
            user.save()
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse(json.dumps(reset_form.errors))


class SendEmailCodeView(LoginRequiredMixin, View):
    '''发送邮箱验证码'''
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在！"}')
        status = send_register_email(email, 'updateemail')
        return HttpResponse('{"status":"发送成功！"}')


class UpdateEmailCode(LoginRequiredMixin, View):
    '''修改个人邮箱'''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        email_code = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='updateemail')
        if email_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse('{"email":"验证码不正确！"}')


class UserCourseView(LoginRequiredMixin, View):
    '''个人中心我的课程'''
    def get(self, request):
        current = 'mycourse'
        user_courses = UserCourse.objects.filter(user=request.user)
        unread_message_num = UserMessage.objects.filter(user=int(request.user.id), has_read=False).count()
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'current': current,
            'unread_message_num': unread_message_num,
        })


class UserFavOrgView(LoginRequiredMixin, View):
    '''个人中心我的收藏课程机构'''
    def get(self, request):
        fav_type = 2
        current = 'org'
        user_fav_org = UserFavorate.objects.filter(user=request.user, fav_type=fav_type )
        # 取出课程机构id
        org_ids = [org.fav_id for org in user_fav_org]
        orgs = CourseOrg.objects.filter(id__in=org_ids)
        unread_message_num = UserMessage.objects.filter(user=int(request.user.id), has_read=False).count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(orgs, 5, request=request)
        orgs = p.page(page)
        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,
            'current': current,
            'unread_message_num': unread_message_num,
        })


class UserFavteacherView(LoginRequiredMixin, View):
    '''个人中心我的收藏授课教师'''
    def get(self, request):
        fav_type = 3
        current = 'teacher'
        user_fav_teacher = UserFavorate.objects.filter(user=request.user, fav_type=fav_type )
        teacher_ids = [teacher.fav_id for teacher in user_fav_teacher]
        teachers = Teacher.objects.filter(id__in=teacher_ids)
        unread_message_num = UserMessage.objects.filter(user=int(request.user.id), has_read=False).count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 5, request=request)
        teachers = p.page(page)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
            'current': current,
            'unread_message_num': unread_message_num,
        })


class UserFavCouerseView(LoginRequiredMixin, View):
    '''个人中心我的收藏公开课程'''
    def get(self, request):
        fav_type = 1
        current = 'course'
        user_fav_course = UserFavorate.objects.filter(user=request.user, fav_type=fav_type )
        course_ids = [course.fav_id for course in user_fav_course]
        courses = Course.objects.filter(id__in=course_ids)
        unread_message_num = UserMessage.objects.filter(user=int(request.user.id), has_read=False).count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, 5, request=request)
        courses = p.page(page)
        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
            'current': current,
            'unread_message_num': unread_message_num,
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        user_message = UserMessage.objects.filter(user=int(request.user.id))
        unread_message_num = UserMessage.objects.filter(user=int(request.user.id), has_read=False).count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_message, 5, request=request)
        user_message = p.page(page)
        return render(request, 'usercenter-message.html', {
            'user_message': user_message,
            'unread_message_num': unread_message_num,
        })
