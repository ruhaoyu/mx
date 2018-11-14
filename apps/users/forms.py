# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/2 17:21'
from django import forms
from captcha.fields import CaptchaField
from users.models import UserProfile


# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=5)
    password = forms.CharField(required=True, max_length=20, min_length=5)


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    # username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, min_length=2, required=True)
    captcha = CaptchaField(error_messages={"invalid": u'验证码错误！'})


# 忘记密码表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u'验证码错误！'})


# 重置密码表单
class ResetFrom(forms.Form):
    password1 = forms.CharField(max_length=20, required=True)
    password2 = forms.CharField(max_length=20, required=True)


# 上传头像表单
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# 修改用户基本资料表单
class ChangeUserInfo(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']
