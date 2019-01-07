# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/3 15:29'
from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from clonemuxue.settings import EMAIL_HOST_USER

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送邮箱验证码
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ""
    email_body = ""
    if send_type == 'register':
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活你的账号： http:148.70.55.181:8000/active/{0}/".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email])
        if send_status:
            return send_status
    if send_type == 'forget':
        email_title = "忘记密码链接"
        email_body = "请点击下面的链接重置密码： http:148.70.55.181:8000/reset/{0}/".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email])

    if send_type == 'updateemail':
        email_title = "修改邮箱验证码"
        email_body = "你的邮箱验证码为： {0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email])