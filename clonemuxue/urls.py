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
from django.views.static import serve
from clonemuxue.settings import MEDIA_ROOT
from users.views import LoginView


urlpatterns = [
    url('^$', LoginView.as_view(), name="login"),
    url(r'^xadmin/', xadmin.site.urls),
    # 用户url配置
    url(r'', include('users.urls')),
    # 组织机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 用户操作url配置
    url(r'^opr/', include('operation.urls', namespace='opr')),
    # 课程url配置
    url(r'^cor/', include('courses.urls', namespace='cor')),
    # 文件上传访问处理
    url('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

    # url('^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
handler403 = 'users.views.page_forbidden'

