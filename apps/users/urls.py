# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/9 12:02'

from django.conf.urls import url, include
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, \
    ForgetPasswordView, ResetView, ModifyView, LogoutView, UsercenterInfoView, ChangeUserImageView
from organization.views import OrgView

urlpatterns = [
    # 首页
    url('^index/$', TemplateView.as_view(template_name='index.html'), name="index"),
    # 登录
    url('^login/$', LoginView.as_view(), name="login"),
    # 注册
    url('^register/$', RegisterView.as_view(), name="register"),
    # 退出
    url('^logout/$', LogoutView.as_view(), name="logout"),
    # 验证码
    url(r'^captcha/', include('captcha.urls')),
    # 激活
    url('^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    # 忘记密码
    url('^forget/$', ForgetPasswordView.as_view(), name="forget_password"),
    # 重置密码
    url('^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset"),
    # 重置密码修改
    url('^modify/$', ModifyView.as_view(), name="modify"),
    # 个人中心
    url('^user_center_info/$', UsercenterInfoView.as_view(), name="usercenterinfo"),
    # 用户头像修改
    url('^user_center_info/change_user_image/$', ChangeUserImageView.as_view(), name="change_user_image"),
    ]