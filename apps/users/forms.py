# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/2 17:21'
from django import forms
from captcha.fields import CaptchaField

# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=5)
    password = forms.CharField(required=True, max_length=20, min_length=5)



# 注册
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    # username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, min_length=2,required=True)
    captcha = CaptchaField(error_messages={"invalid": u'验证码错误！'})
