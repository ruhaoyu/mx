# _*_ encoding:utf-8 _*_
"""clonemuxue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPasswordView, ResetView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 首页
    url('^index/$', TemplateView.as_view(template_name='index.html'), name="index"),
    # 登录
    url('^login/$', LoginView.as_view(), name="login"),
    # 注册
    url('^register/$', RegisterView.as_view(), name="register"),
    # 验证码
    url(r'^captcha/', include('captcha.urls')),
    # 激活
    url('^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    # 忘记密码
    url('^forget/$', ForgetPasswordView.as_view(), name="forget_password"),
    # 重置密码
    url('^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset"),
]
