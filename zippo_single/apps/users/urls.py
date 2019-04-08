# coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/27'

from django.conf.urls import  url, include
from users import views
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEamilCodeView, UpdateEmailView #Return_City_DataView, Return_Store_DataView
#from .views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView


urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEamilCodeView.as_view(), name="sendemail_code"),
    # url(r'^active/(?P<active_code>[a-zA-Z0-9]{16})/$', ActiveUserView.as_view(), name='active_user'),
    # 修改邮箱
    #url(r'^GetCityData/$',Return_City_DataView.as_view(),name="GetCityData"),
    #url(r'^GetStoreData/$',Return_Store_DataView.as_view(),name="GetStoreData"),
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    #url(r'^userinfo/add/$', views.userinfo_add),
    #url(r'^userinfo/del/(\d+)/$', views.userinfo_del),
    #url(r'^userinfo/edit/(\d+)/$', views.userinfo_edit),
    # 我的课程
#    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),

    # 我收藏的课程机构
#   url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),

    # 我收藏的讲师
#   url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我收藏的课程
#   url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息
#   url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),
]
