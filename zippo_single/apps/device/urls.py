
# coding:utf-8


from django.conf.urls import url, include
from .views import WebsocketView,ResourceView,SoftwareView,StatusView,StatusAuthView,StatushomeAuthView,StatusdetailView,StatustableView,StatustabledetailView

urlpatterns = [
    url(r'^resource/$', ResourceView.as_view(), name="device_resource"),
    #url(r'^resource/(\d+)/(\d+)/(\d+)/$', ResourceAuthView.as_view(), name="device_auth_resource"),
    url(r'^time/$', WebsocketView.as_view(), name="time"),
    #url(r'^resource_update/$', ResourceUpdateView.as_view(), name="resource_update"),
    url(r'^software/$', SoftwareView.as_view(), name="update_software"),
    #url(r'^software/(\d+)/(\d+)/(\d+)/$', SoftwareAuthView.as_view(), name="update_auth_software"),
    #url(r'^software_update/$', SoftwareUpdateView.as_view(), name="software_update"),
    url(r'^status/$', StatusView.as_view(), name="status"),
    url(r'^status/(\d+)/(\d+)/(\d+)/(\d+)/$', StatusAuthView.as_view(), name="auth_status"),
    url(r'^statushome/(\d+)/(\d+)/(\d+)/(\d+)/$', StatushomeAuthView.as_view(), name="auth_status"),
    url(r'^statusdetail/$', StatusdetailView.as_view(), name="detail_status"),
    url(r'^table/(\d+)/(\d+)/(\d+)/(\d+)/$',StatustableView.as_view(), name="table_status"),
    url(r'^tabledetail/(\d+)/(\d+)/(\d+)/(\d+)/$',StatustabledetailView.as_view(), name="tabledetail_status")
]
