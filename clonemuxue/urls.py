# _*_ encoding:utf-8 _*_

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework import routers, serializers, viewsets
from rest_framework.documentation import include_docs_urls

from clonemuxue.settings import MEDIA_ROOT
from users.views import LoginView
from users.models import UserProfile


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='mx')),
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
