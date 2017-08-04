# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm
from utils.email_send import send_register_email

# Create your views here.


# 重新定义认证，使邮箱也可以登录
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 注册
class RegisterView(View):
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

# 激活
class ActiveUserView(View):
    def get(self, request, active_code):
        email_code = EmailVerifyRecord.objects.get(code=active_code)
        email = email_code.email
        user_profile = UserProfile.objects.get(username=email)
        # 激活时判断url是否存在
        if email_code:
            user_profile.is_active = True
            user_profile.save()
        return render(request, "login.html")


# 登录
class LoginView(View):
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


# 找回密码
class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            user_profile = UserProfile()
            try:
                user_data = UserProfile.objects.filter(username=email)
            except:
                user_data = None
            # 判断用户是否存在
            if user_data:
                send_register_email(email, "forget")
                return render(request, 'forget_email_succese.html')
            else:
                return render(request, "forgetpwd.html", {'forget_form': forget_form, 'msg': '用户不存在！'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        email_code = EmailVerifyRecord.objects.filter(code = reset_code)
        code = email_code.code


