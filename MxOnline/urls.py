"""MxOnline URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve
from users.views import *

from MxOnline.settings import MEDIA_ROOT,STATIC_ROOT
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #添加验证码的url
    url(r'^captcha/', include('captcha.urls')),
    url(r"^$",IndexView.as_view(), name='index'),
    url(r"^login/$",LoginView.as_view(), name='login'),
    url(r"^logout/$",LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    #处理邮箱验证的url
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='user_active'),
    #找回密码处理:
    url(r'^froget/$',ForgetPwView.as_view(),name='forget_pwd'),
   #重置密码:
    url(r"^reset/(?P<reset_code>.*)/$",ResetView.as_view(),name='reset_pwd'),
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),
    # url(r"^org_list/$",OrgView.as_view(),name="org_list"),
    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),
    #配置static
    # url(r'^static/(?P<path>.*)',serve,{'document_root':STATIC_ROOT}),

    #课程机构url配置
    url(r'^org/',include('organization.urls',namespace='org')),
    #课程相关url配置
    url(r'^course/',include('courses.urls',namespace='course')),

    url(r'^users/',include('users.urls',namespace='users')),

    #富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls'))
]


#全局404页面配置
handler404 ='users.views.page_not_found'
handler500 ='users.views.page_orror'
handler403 ='users.views.page_orror'