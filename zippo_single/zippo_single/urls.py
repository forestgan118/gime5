"""zippo_single URL Configuration

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
from django.views.static import serve
#from django.urls import path

from django.views.generic import TemplateView
from zippo_single.settings import MEDIA_ROOT
from users.views import IndexHomeView,IndexAuthView,LoginView, RegisterView, ActiveUserView, ForgetPwdView, RestView, ModifyPwdView, LogoutView ,IndexView
from organization.views import download,OrgView,Return_City_DataView, Return_Store_DataView 
import xadmin
#from users.views import Return_City_Data, Return_Store_Data
from device.views import mac_data
from macdata.views import home
from apscheduler.scheduler import Scheduler
import time
#from macdata.views import mac_data#假设我要执行的函数时app01项目下的views.py中的aaa函数

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^index/$', IndexView.as_view(),name="index"),
    url(r'^index/(\d+)/(\d+)/(\d+)/(\d+)/$', IndexAuthView.as_view(), name="index_auth"),
    url(r'^home/$', IndexHomeView.as_view(),name="index_home"),
    #url(r'^GetCityData/$',Return_City_DataView.as_view(),name="GetCityData"),
    #url(r'^GetStoreData/$',Return_Store_DataView.as_view(),name="GetStoreData"),
    # 用户
#    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^login/$', LoginView.as_view(), name="login"),
    # 不安全的sql注入
    # url('^login/', LoginUnsafeView.as_view(), name='login'),
    #url(r'^csv/$', Csv_ExportView.as_view(),name="csv"),
    # 验证码 url配置
    url(r'^captcha/', include('captcha.urls')),
    # 退出功能url
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    # 注册url
    url(r'^register/$', RegisterView.as_view(), name="register"),
    # 激活用户url
    url(r'^active/(?P<active_code>.*)/$',
        ActiveUserView.as_view(), name="user_active"),
    # 忘记密码
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    # 重置密码urlc ：用来接收来自邮箱的重置链接
    url(r'^reset/(?P<active_code>.*)/$', RestView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构URL配置
    url(r'^org/', include('organization.urls', namespace="org")),
    url(r'^device/', include('device.urls', namespace="device")),
    #url(r'^userinfomation/$', UserInfomationView.as_view(), name="userinfomation"),
    #url(r'^userinfomation_add/$', UserInfomation_addView.as_view(), name="userinfomation_add"),
    #url(r'^userinfomation_del/$', UserInfomation_delView.as_view(), name="userinfomation_del"),
    #url(r'^userinfomation_edit/$', UserInfomation_editView.as_view(), name="userinfomation_edit"),
    # 课程列表
#    url(r'^course/', include('courses.urls', namespace="course")),

#    url(r'^djcelery/', include('djcelery.urls')),
    # 用户
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^dsky', home),
    url(r'^download', download),
    #url(r'^rbac/', include('rbac.urls', namespace="rbac")),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    #url(r'dsky', home),
#    url(r'^device/', include('device.urls', namespace="device")),
]

sched = Scheduler()  #实例化，固定格式
sched1 = Scheduler()  #实例化，固定格式
#sched.daemonic = False
sched.start()  #定时器启动  必须
#sched1.start()  #定时器启动  必须
#@sched.interval_schedule(seconds=5, start_date='2018-07-25 12:11:00')  #装饰器，seconds=60意思为该函数为1分钟运行一次
#@sched.interval_schedule(minutes=1)  #装饰器，seconds=60意思为该函数为1分钟运行一次
#@sched.interval_schedule(seconds=3)  #装饰器，seconds=60意思为该函数为1分钟运行一次

def timed_job():
    mac_data()

#    print('This job is run every three minutes.')
#@sched.scheduled_job('cron', day_of_week='mon-fri', hour='0-9', minute='30-59', second='*/3')
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')
#sched.add_interval_job(timed_job, hours=24, start_date='2018-10-18 00:05:00')  #定时任务加入   必须
sched.add_interval_job(timed_job, seconds=20, start_date='2019-02-06 00:00:42')  #定时任务加入   必须
#sched1.add_interval_job(timed_job1, seconds=20, start_date='2019-02-06 00:00:42')  #定时任务加入   必须

