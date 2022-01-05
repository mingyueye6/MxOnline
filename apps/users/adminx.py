#_*_utf-8_*_
import xadmin
from .models import *
from xadmin import views
#设置后台管理系统的全局变量
from xadmin.plugins.auth import UserAdmin

class UserProfileAdmin(UserAdmin):
    pass


class BaseSetting(object):
    #设置主题工功能:默认是False
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    #更改后天管理系统的首页题目
    site_title = "暮学后台管理系统"
    site_footer = "暮学在线"
    #将每个表中的字段折叠
    menu_style = 'accordion'




class EmailVerifyRecordAdmin(object):
    #修改后台图标的照片
    model_icon = 'fa fa-address-book-o'
    list_display = ["code","email","send_type","send_time"]
    search_fields = ["code","email","send_type"]
    list_filter = ["code","email","send_type","send_time"]


class BannerAdmin(object):
    #后台显示的字段
    list_display = ["title","image","index","url","add_time"]
    search_fields = ["title","image","index","url",]
    list_filter = ["title","image","index","url","add_time"]





xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
#注册Basesetting
xadmin.site.register(views.BaseAdminView,BaseSetting)
#注册GlobalSetting
xadmin.site.register(views.CommAdminView,GlobalSetting)
# xadmin.site.unregister()
# xadmin.site.register(UserProfile,UserProfileAdmin)
