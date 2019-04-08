"""data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.conf.urls import path
from django.conf.urls import url,include
from macdata.views import home
from apscheduler.scheduler import Scheduler
import time
from macdata.views import mac_data#假设我要执行的函数时app01项目下的views.py中的aaa函数
'''
urlpatterns = [
#    path('admin/', admin.site.urls),
    url(r'^dsky/', home),	
]


sched = Scheduler()  #实例化，固定格式
#@sched.interval_schedule(seconds=)  #装饰器，seconds=60意思为该函数为1分钟运行一次
@sched.interval_schedule(minutes=1)  #装饰器，seconds=60意思为该函数为1分钟运行一次
def timed_job():
    mac_data()
#    print('This job is run every three minutes.')
#@sched.scheduled_job('cron', day_of_week='mon-fri', hour='0-9', minute='30-59', second='*/3')
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')

sched.start()
'''