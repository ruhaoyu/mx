# _*_ encoding:utf-8 _*_
__author__ = 'yuruhao'
__date__ = '2017/7/27 16:36'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner, UserProfile



# 主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
# 全局
class GlobalSetting(object):
    site_title = u'慕学后台管理系统'
    site_footer = u'来自小白余汝浩的项目'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ('code', 'email', 'send_type', 'send_time')
    search_fields = ('code', 'email', 'send_type')
    list_filter = ('code', 'email', 'send_type', 'send_time')
    model_icon = 'fa fa-bookmark-o'


class BannerAdmin(object):
    list_display = ('title', 'image', 'url', 'index', 'add_time')
    search_fields = ('title', 'image', 'url', 'index')
    list_filter = ('title', 'image', 'url', 'index', 'add_time')
    model_icon = 'fa fa-barcode'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
