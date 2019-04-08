
# coding:utf-8


from django.conf.urls import url, include
from .views import DetailSelectView,OrgView,Return_City_DataView, Return_Store_DataView,Return_Province_DataView, DetailView,DetailAuthView,DetailtableView
# from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
# from .views import TeacherListView, TeacherDetailView


urlpatterns = [
    # 课程机构列表
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    #url(r'^index/$',IndexView.as_view(), name="index"),
    url(r'^GetProvinceData/$',Return_Province_DataView.as_view(),name="GetProvinceData"),
    url(r'^GetCityData/$',Return_City_DataView.as_view(),name="GetCityData"),
    url(r'^GetStoreData/$',Return_Store_DataView.as_view(),name="GetStoreData"),
    #url(r'^csv/$', Csv_ExportView.as_view(),name="csv"),
    url(r'^detail/$', DetailView.as_view(), name="device_detail"),
    url(r'^detail/(\d+)/(\d+)/(\d+)/(\d+)/$', DetailAuthView.as_view(), name="device_auth_detail"),
    url(r'^detailselect/(\d+)/(\d+)/(\d+)/(\d+)/$', DetailSelectView.as_view(), name="device_select_detail"),
    url(r'^table/(\d+)/(\d+)/(\d+)/(\d+)/$', DetailtableView.as_view(), name="device_table_detail")
    
    #url(r'^table/$', DetailtableView.as_view(), name="device_table_detail")
    #    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    #    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    #    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    #    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    #    url(r'^org_teacher/(?P<org_id>\d+)/$',
    #        OrgTeacherView.as_view(), name="org_teacher"),

    # 机构收藏
    #    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 讲师列表
    #    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),

    # 讲师详情
    #    url(r'^teacher/detail/(?P<teacher_id>\d+)/$',
    #        TeacherDetailView.as_view(), name="teacher_detail"),

]
