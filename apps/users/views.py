# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm
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
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html',{'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        pass



# 登录
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_active = UserProfile.objects.get(username=user_name)
            if user_active is True:
                user = authenticate(username=user_name, password=pass_word)
                if user is not None:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {'msg': '用户名或密码错误！'})
            else:
                return render(request, 'login.html', {'msg': '用户未激活，请激活后再重新登录！'})
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