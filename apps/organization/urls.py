# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/8/9 12:24'


from django.conf.urls import url
from organization.views import OrgView, OrgHomeView, OrgCourseView, OrgDetailView, OrgTeacherView, AddFavView, TeacherView

urlpatterns = [
    # 课程机构首页
    url('^list/$', OrgView.as_view(), name="org_list"),
    url('^home/(?P<org_id>\d+)$', OrgHomeView.as_view(), name="org_home"),
    url('^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name="org_course"),
    url('^detail/(?P<org_id>\d+)$', OrgDetailView.as_view(), name="org_detail"),
    url('^teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏
    url('^add_fav/$', AddFavView.as_view(), name="add_fav"),
    # 授课教师列表页
    url('^teacher/$', TeacherView.as_view(), name='teacher_list'),
        ]