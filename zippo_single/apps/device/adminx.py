# /usr/bin/python
# coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/8'


from crispy_forms.layout import Fieldset
from django.contrib.auth.models import Group, Permission
#from operation.models import CourseComments, UserFavorite, UserMessage, UserCourse, UserAsk
#from organization.models import CityDict, Teacher, CourseOrg
from xadmin.layout import Main, Row, Side
from xadmin.models import Log
from xadmin.plugins.auth import UserAdmin
from django.utils.translation import ugettext as _

import xadmin
from xadmin import views
#from courses.models import Course, Lesson, Video, CourseResource
from .models import Mqtt,InteractInfo, DeviceStatus, SatisfactionData, wifiprobeData, SatisfactionData_day, SatisfactionData_week, SatisfactionData_month,SatisfactionData_quarter,SatisfactionData_year,wifiprobeData_day,wifiprobeData_week,wifiprobeData_month,wifiprobeData_quarter,wifiprobeData_year


# 创建X admin的全局管理器并与view绑定。
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# x admin 全局配置参数信息设置
class GlobalSetting(object):
    site_title = "后台管理"
    site_footer = "zippo admin"
    menu_style = "accordion"

class MqttAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'login_name', 'password','port','keepAlive']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name', 'login_name', 'password','port','keepAlive']
    # 配置筛选字段
    list_filter = ['name', 'login_name', 'password','port','keepAlive']
    model_icon = 'fa fa-envelope'


class InteractInfoAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'login_name', 'mac', 'device_id','ip','software_name','ver','utime']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name', 'login_name', 'mac', 'device_id','ip','software_name','ver','utime']
    # 配置筛选字段
    list_filter = ['name', 'login_name', 'mac', 'device_id','ip','software_name','ver','utime']
    model_icon = 'fa fa-envelope'

class DeviceStatusAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'device_id','pram1_status','pram2_status','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name', 'device_id','pram1_status','pram2_status','add_time']
    # 配置筛选字段
    list_filter = ['name', 'device_id','pram1_status','pram2_status','add_time']
    model_icon = 'fa fa-envelope'


class SatisfactionDataAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置筛选字段
    list_filter = ['name', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    model_icon = 'fa fa-envelope'

class wifiprobeDataAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['device_id','wifi_3m_num','wifi_1m_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['device_id','wifi_3m_num','wifi_1m_num','add_time']
    # 配置筛选字段
    list_filter = ['device_id','wifi_3m_num','wifi_1m_num','add_time']
    model_icon = 'fa fa-envelope'

class SatisfactionData_dayAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'time','device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置筛选字段
    list_filter = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    model_icon = 'fa fa-envelope'

class SatisfactionData_weekAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'time','device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置筛选字段
    list_filter = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    model_icon = 'fa fa-envelope'

class SatisfactionData_monthAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'time','device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置筛选字段
    list_filter = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    model_icon = 'fa fa-envelope'

class SatisfactionData_quarterAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'time','device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置筛选字段
    list_filter = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    model_icon = 'fa fa-envelope'

class SatisfactionData_yearAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['name', 'time','device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    # 配置筛选字段
    list_filter = ['name','time', 'device_id','excellent_num','good_num','unsatisfy_num','add_time']
    model_icon = 'fa fa-envelope'

class wifiprobeData_dayAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置筛选字段
    list_filter = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    model_icon = 'fa fa-envelope'

class wifiprobeData_weekAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置筛选字段
    list_filter = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    model_icon = 'fa fa-envelope'

class wifiprobeData_monthAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置筛选字段
    list_filter = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    model_icon = 'fa fa-envelope'

class wifiprobeData_quarterAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置筛选字段
    list_filter = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    model_icon = 'fa fa-envelope'

class wifiprobeData_yearAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    # 配置筛选字段
    list_filter = ['device_id','time','wifi_3m_num','wifi_1m_num','add_time']
    model_icon = 'fa fa-envelope'


# 将model与admin管理器进行关联注册
xadmin.site.register(Mqtt, MqttAdmin)
xadmin.site.register(InteractInfo, InteractInfoAdmin)
xadmin.site.register(DeviceStatus, DeviceStatusAdmin)
xadmin.site.register(SatisfactionData, SatisfactionDataAdmin)
xadmin.site.register(wifiprobeData, wifiprobeDataAdmin)
xadmin.site.register(SatisfactionData_day, SatisfactionData_dayAdmin)
xadmin.site.register(wifiprobeData_day, wifiprobeData_dayAdmin)
xadmin.site.register(SatisfactionData_week, SatisfactionData_weekAdmin)
xadmin.site.register(wifiprobeData_week, wifiprobeData_weekAdmin)
xadmin.site.register(SatisfactionData_month, SatisfactionData_monthAdmin)
xadmin.site.register(wifiprobeData_month, wifiprobeData_monthAdmin)
xadmin.site.register(SatisfactionData_quarter, SatisfactionData_quarterAdmin)
xadmin.site.register(wifiprobeData_quarter, wifiprobeData_quarterAdmin)
xadmin.site.register(SatisfactionData_year, SatisfactionData_yearAdmin)
xadmin.site.register(wifiprobeData_year, wifiprobeData_yearAdmin)
# 将全局配置管理与view绑定注册
#xadmin.site.register(views.BaseAdminView, BaseSetting)
# 将头部与脚部信息进行注册:
#xadmin.site.register(views.CommAdminView, GlobalSetting)
