# _*_ encoding:utf-8 _*_

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from clonemuxue.settings import MEDIA_ROOT
from users.views import LoginView

urlpatterns = [
    url('^$', LoginView.as_view(), name="login"),
    url(r'^admin/', admin.site.urls),
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
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url('', include('social_django.urls', namespace='social'))

    # url('^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
handler403 = 'users.views.page_forbidden'
