# coding:utf-8
import json
import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,render_to_response
from django.core.urlresolvers import reverse
#from django.core.context_processors import request
# Django自带的用户验证,login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.core import serializers
from datetime import date
from datetime import datetime
# 进行密码加密
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse, HttpResponseRedirect
from itertools import chain
# 并集运算
from django.db.models import Q
# 基于类实现需要继承的view
from django.views.generic.base import View
from .models import UserProfile, EmailVerifyRecord
# form表单验证 & 验证码
from .forms import LoginForm, ActiveForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
# 发送邮件
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin
#from operation.models import  UserCourse, UserFavorite, UserMessage
from operation.models import UserMessage
from organization.models import  RegionDict, CityDict, Store , SaleProduct_day, SaleAccessory_day
from device.models import wifiprobeData_day, SatisfactionData_day
from apps.rbac.models import UserInfo
import re
from rbac.service.init_permission import init_permission
 
# from courses.models import Course
#from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


# 实现用户名邮箱均可登录
# 继承ModelBackend类，因为它有方法authenticate，可点进源码查看
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            # Q为or值，用户名=输入的用户名，或者邮箱等于输入的邮箱
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            print(user)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_records:
            for record in all_records:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "signin.html", )
        else:
            # return render(request, "active_fail.html")
            return render(
                request, "signup.html", {
                    "msg": "您的激活链接无效", "active_form": active_form})
        # return render(request, "login.html")


class RegisterView(View):
    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, "signup.html",
                      {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 这里注册时前端的name为email
            nick_name = request.POST.get("nick", "")
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            if UserProfile.objects.filter(Q(email=user_name) and Q(username=user_name) and Q(nick_name=nick_name)): #确保用户名与email都不重复
#            if UserProfile.objects.filter(email=user_name):
                print ("重名")
                return render(request, "signup.html",
                              {"register_form": register_form, "msg": "用户已存在"})
            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.nick_name = nick_name
            user_info=UserInfo()
            user_info.name=nick_name
            user_info.email=user_name
            # 默认激活状态为false
            user_profile.is_active = False
            # 对明文密码进行加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            user_info.password = make_password(pass_word)
            user_info.save()
            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册"
            user_message.save()

            send_register_email(user_name, "register")
            # 跳转到登录页面
            return render(request, "signin.html", {"msg": "请前往注册邮箱进行激活"})
        # 注册邮箱form验证失败
        else:
            return render(request, "signup.html",
                          {"register_form": register_form})
class BasePagPermission(object):
    def __init__(self, code_list):
        self.code_list = code_list

    def has_add(self):
        if "add" in self.code_list:
            return True

    def has_del(self):
        if "del" in self.code_list:
            return True

    def has_edit(self):
        if "edit" in self.code_list:
            return True


class LoginView(View):
    # 直接调用get方法免去判断
    
    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        redirect_url = request.GET.get('next', '')
        #print ("get index")
        return render(request, "signin.html", {"redirect_url": redirect_url
        })
        
    def post(self, request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
        # POST中的usernamepassword，会对应到form中
        login_form = LoginForm(request.POST)
        # LoginForm()在传进来的时候有一个参数，这个参数为字典，request.POST就是一个字典
        # 所以此处一般传入request.POST内容
        # is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面name值
            email_login = request.POST.get("username", "")
            #print (email_login)
            pass_word = request.POST.get("password", "")
            #print (pass_word)
            user_profile = authenticate(username=email_login, password=pass_word)
            print (user_profile)
            if user_profile is not None:
                # 只有当用户激活时才给登录
                if user_profile.is_active:
                    user = UserInfo.objects.filter(email=email_login).first()
                    print ("user=",user)
                    if user:
                        init_permission(user, request)
                        #return HttpResponseRedirect("/userinfomation/")
                        return HttpResponseRedirect("/home/")
                    else:
                        return render(request, "signin.html", {"login_form": login_form})
                else:
                        return render(request, "signin.html", {"login_form": login_form})
                #else:
                #    return render(request, "signin.html", {"msg": "用户未激活!请前往邮箱进行激活"})
                '''
                # 成功返回user对象,失败返回null
                #user = authenticate(username=user_name, password=pass_word)
                # 如果不是null说明验证成功
                #if user is not None:
                # 只有当用户激活时才给登录
                if user.is_active:
                    # login_in 两参数：request, user
                    # 实际是对request写了一部分东西进去，然后在render的时候：
                    # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页
                    # 跳转到首页 user request会被带回到首页
                    # 增加重定向回原网页。
                    #redirect_url = request.POST.get('next', '')
                    return redirect('/index/')
                    #if redirect_url:
                    #    return HttpResponseRedirect(redirect_url)
                    # from django.core.urlresolvers import reverse
                    #return HttpResponseRedirect(reverse("index"))
                    # return render(request, "index.html")
                # 即用户未激活跳转登录，提示未激活
                else:
                    return render(request, "signin.html", {"msg": "用户未激活!请前往邮箱进行激活"})
                '''
                # 仅当用户真的密码出错时
            elif user_profile is None:
                return render(request, "signin.html", {"msg": "用户名密码错误"})
            
            # 验证不成功跳回登录页面
            # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(request, "signin.html", {"login_form": login_form})


class IndexHomeView(View):
    # 直接调用get方法免去判断
    
    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        redirect_url = request.GET.get('next', '')
        #print ("get index")
        return render(request, "home.html", {"redirect_url": redirect_url
        })


'''
class UserInfomationView(View):
	def get(self,request):
		pagpermission = BasePagPermission(request.permission_code_url)  # 实例化
		# print("code......", request.permission_code_url)
		data_list = [
			{"id": 1, "name": "forest.gan@gime5.cn"},
			{"id": 2, "name": "forest.gan@gime5.cn"},
			{"id": 3, "name": "haiyan3"},
			{"id": 4, "name": "haiyan4"},
			{"id": 5, "name": "haiyan5"},
		]
		#print("data_list",data_list)
		#print("pagpermission",pagpermission)
		return render(request, "userinfo.html", {"data_list": data_list, "pagpermission": pagpermission})
'''
'''
class UserInfomation_addView(View):
	def get(self,request):
		if request.method == "GET":
			return render(request,"userinfo_add.html")
		else:
			return redirect("/userinfo/")

class UserInfomation_delView(View):
	def get(request, nid):
		return HttpResponse("删除用户")

class UserInfomation_editView(View):
	def userinfo_edit(request, nid):
		return HttpResponse("编辑用户")
'''

'''
# 开始用类来写登入逻辑，LoginView类，所以这个user_login函数已丢弃
# 当我们配置url被这个view处理时，自动传入request对象.
def user_login(request):
    # 前端向后端发送的请求方式: get 或post

    # 登录提交表单为post
    if request.method == "POST":
        # 取不到时为空，username，password为前端页面name值
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        # 成功返回user对象,失败返回null
        user = authenticate(username=user_name, password=pass_word)

        # 如果不是null说明验证成功
        if user is not None:
            # login_in 两参数：request, user
            # 实际是对request写了一部分东西进去，然后在render的时候：
            # request是要render回去的。这些信息也就随着返回浏览器。完成登录
            login(request, user)
            # 跳转到首页 user request会被带回到首页
            return render(request, "index.html")
        # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(request, "signin.html", {"msg": "用户名或密码错误！"})
    # 获取登录页面为get
    elif request.method == "GET":
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "signin.html", {})
'''

class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("signin.html"))


# 用户忘记密码的处理view
class ForgetPwdView(View):
    # get方法直接返回页面
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    # post方法实现
    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        # form验证合法情况下取出email
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送找回密码邮件
            print(email)
            send_register_email(email, "forget")
            # 发送完毕返回登录页面并显示发送邮件成功。
            return render(request, "signin.html", {"msg": "重置密码邮件已发送,请注意查收"})
        # 如果表单验证失败也就是他验证码输错等。
        else:
            return render(request, "forgetpwd.html",
                          {"forget_form": forget_form})


# 重置密码的view
class RestView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_records:
            for record in all_records:
                # 获取到对应的邮箱
                email = record.email
                # 将email传回来
                return render(request, "password_reset.html", {"email": email})
        # 自己瞎输的验证码
        else:
            return render(request, "forgetpwd.html", {
                "msg": "您的重置密码链接无效,请重新请求", "active_form": active_form})
        # return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(request, "password_reset.html",
                              {"email": email, "msg": "密码不同"})
            # 如果密码一致
            user = UserProfile.objects.get(email=email)
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return render(request, "signin.html", {"msg": "密码修改成功，请登录"})
        # 验证失败说明密码位数不够。
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html",
                          {"email": email, "modifypwd_form": modifypwd_form})


class UserInfoView(LoginRequireMixin, View):
    """
    用户个人信息
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "profile.html", {})

    def post(self, request):
        # 不像用户咨询是一个新的。需要指明instance。不然无法修改，而是新增用户
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        """
        instance:这是个关键参数
        这里是使用了model form，所以需要instance参数，来指明用了哪个实例（哪条数据）来修改
        """
        print(user_info_form)
        if user_info_form.is_valid():
            user_info_form.save()
            print("修改成功")
            return HttpResponse('{"status": "success", "msg":"修改成功"}',
                                content_type="application/json")
        else:
            # 通过json的dumps方法把字典转换为json字符串
            print("修改不成功")
            print (user_info_form.errors)
            return HttpResponse(json.dumps(user_info_form.errors),
                                content_type="application/json")
        """
        json.dump(user_info_form.errors):获取了cleaned_data的错误信息
        """


# 用户上传图片的view:用于修改头像
class UploadImageView(LoginRequireMixin, View):
    """
    用户修改头像
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        # 这时候用户上传的文件就已经被保存到imageform了 ，为modelform添加instance值直接保存
        image_form = UploadImageForm(
            request.POST, request.FILES, instance=request.user)

        if image_form.is_valid():

            image_form.save()
            # # 取出cleaned data中的值,一个dict
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}',
                                content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg":"修改失败"}',
                                content_type="application/json")


class UpdatePwdView(View):
    """
    个人中心密码修改
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg":"密码不一致"}',
                                    content_type="application/json")
            # 如果密码一致
            user = request.user
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}',
                                content_type="application/json")
        else:
            # 通过json的dumps方法把字典转换为json字符串
            return HttpResponse(json.dumps(modify_form.errors),
                                content_type="application/json")


class SendEamilCodeView(LoginRequireMixin, View):
    """
    发送邮箱验证码
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        # 取出需要发送的邮件
        email = request.GET.get("email", "")
        # 不能是已注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在"}',
                                content_type="application/json")
        send_register_email(email, "update_email")
        return HttpResponse('{"status": "success", "msg":"修改成功"}',
                            content_type="application/json")


class UpdateEmailView(LoginRequireMixin, View):
    """
        修改个人邮箱
        """
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(
            email=email, code=code, send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}',
                                content_type="application/json")
        else:
            return HttpResponse('{"email": "验证码出错"}',
                                content_type="application/json")




class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)
#我们自定义一个类试试 
class User(object): 
    def __init__(self, name): 
        self.name = name 

class UserEncoder(json.JSONEncoder): 
    def default(self, obj): 
        if isinstance(obj, User): 
          return obj.name 
        return json.JSONEncoder.default(self, obj)

class Return_City_DataView(View):
    def get(self,request):
        all_city=CityDict.objects.all()
        all_region = RegionDict.objects.all()
        region_id = request.GET['region']
        all_city = all_city.filter(region_id=int(region_id))
        print (region_id)
        City_list = []
        for city in all_city:
            City_list.append(city.name)
        return HttpResponse(json.dumps(City_list))    

class Return_Store_DataView(View):
    def get(self,request):
        all_city=CityDict.objects.all()
        all_store=Store.objects.all()
        all_region = RegionDict.objects.all()
        region_id,city_name = request.GET['region'],request.GET['City']
        print (region_id,city_name)
        select_region=all_region.filter(id=int(region_id))
        select_city=all_city.filter(name=str(city_name))
        Store_list=[]
        for city in select_city:
            select_store=all_store.filter(city__id=int(city.id))
        for store in select_store:
            Store_list.append(store.name)
        return HttpResponse(json.dumps(Store_list))



class IndexView(LoginRequireMixin,View):
    """
    首页
    """
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self, request):
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        #all_city = CityDict.objects.all()
        return render(request, "index.html",{"all_region":all_region})
    
    def  post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()
        select_region=""
        select_city=""
        select_store=""
        data1=""
        data2=""
        data3=""
        data4=""
        data5=""
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        
        region_id=request.POST.get('region',"")
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        day_id=int(request.POST.get('day_select',""))
        print (region_id,city_id,store_id,day_id)
        region_select = all_region.filter(name=str(region_id))
        city_select = all_city.filter(name=str(city_id))
        store_select = all_store.filter(name=str(store_id))
        print (region_select,city_select,store_select,day_id)
        if region_id and city_id and store_id and day_id==7:
            product=SaleProduct_day.objects.filter(store=store_select.values('name')).values('time','sum_pro','sum_acc').order_by('time')
            wifi_1m=wifiprobeData_day.objects.filter(device_id=store_select.values('device_id')).values('time','wifi_1m_num').order_by('time')
            wifi_3m=wifiprobeData_day.objects.filter(device_id=store_select.values('device_id')).values('time','wifi_3m_num').order_by('time')
            quantity=SaleProduct_day.objects.filter(store=store_select.values('name')).values('time','quantity_pro','quantity_acc').order_by('time')
            satisfy=SatisfactionData_day.objects.filter(device_id=store_select.values('device_id')).values('time','excellent_num','good_num','unsatisfy_num').order_by('time')
            series1=json.dumps(list(product),cls=JsonCustomEncoder)
            series2=json.dumps(list(wifi_1m),cls=JsonCustomEncoder)
            series3=json.dumps(list(wifi_3m),cls=JsonCustomEncoder)
            series4=json.dumps(list(quantity),cls=JsonCustomEncoder)
            series5=json.dumps(list(satisfy),cls=JsonCustomEncoder)
            data1=json.dumps(series1)
            data2=json.dumps(series2)
            data3=json.dumps(series3)
            data4=json.dumps(series4)
            data5=json.dumps(series5)
            return render(request, "index.html",
                {"all_region":all_region,
                 #"all_province":all_province,
                 "all_city": all_city,
                 "region_id":region_id,
                 "city_id":city_id,
                 #"store_id":store.id,
                 #"select_store":select_store,
                 "select_region":select_region,
                 #"select_city":select_city,
                 "all_store": all_store,
                 'Series1' : json.dumps(data1),
                 'Series2' : json.dumps(data2),
                 'Series3' : json.dumps(data3),
                 'Series4' : json.dumps(data4),
                 'Series5' : json.dumps(data5)
                 })
        elif region_id and city_id and store_id=="" :
            all_store = all_store.filter(city_id=int(city_id))
            select_city=all_city.filter(id=int(city_id))
            print(select_city)
            print (city_id)
            return render(request, "data_review.html",
                {"all_region":all_region,
                 #"all_province":all_province,
                 "all_city": all_city,
                 "region_id":region_id,
                 "city_id":city_id,
                 #"store_id":store.id,
                 #"select_store":select_store,
                 "select_region":select_region,
                 #"select_city":select_city,
                 "all_store": all_store,
                 'Series1' : json.dumps(data1),
                 'Series2' : json.dumps(data2),
                 'Series3' : json.dumps(data3),
                 'Series4' : json.dumps(data4),
                 'Series5' : json.dumps(data5)
                 })
        elif region_id and city_id=="" and store_id=="":
            select_store = all_store.filter(id=int(store_id))
            print(select_store)
            #print(select_store.values('name'))
            #Sale_Product = SaleProduct.objects.all()
            #Sale_Accessory = SaleAccessory.objects.all()
            product=SaleProduct_day.objects.filter(store=select_store.values('name')).values('time','sum_pro','sum_acc').order_by('time')
            wifi_1m=wifiprobeData_day.objects.filter(device_id=select_store.values('device_id')).values('time','wifi_1m_num').order_by('time')
            wifi_3m=wifiprobeData_day.objects.filter(device_id=select_store.values('device_id')).values('time','wifi_3m_num').order_by('time')
            quantity=SaleProduct_day.objects.filter(store=select_store.values('name')).values('time','quantity_pro','quantity_acc').order_by('time')
            print (quantity)
            satisfy=SatisfactionData_day.objects.filter(device_id=select_store.values('device_id')).values('time','excellent_num','good_num','unsatisfy_num').order_by('time')
            #access=SaleAccessory_day.objects.filter(store=select_store.values('name')).values('sum_acc').order_by('time')
            #print (access)
            #product1=chain(product,access)
            #sale_access=SaleAccessory_day.objects.filter(store=select_store.values('name'))
            #print (product)
            #sale_product_select=sale_product.store.filter(store=str(select_store))
            #print (sale_product_select)
            #sale_time_pro=serializers.serialize('json',sale_product.values('time'))
            #sale_time_access=serializers.serialize(sale_access.values('time'))
            #time_sale=sale_time_pro.values('time')
            #print (sale_time_pro)
            #all_dicts=toDicts(all_objs)
            #sale_sum_pro=json.dumps(sale_product.values('sum'))
            #sale_sum_access=json.dumps(sale_access.values('sum'))
            #print (sale_sum_access)
            series1=json.dumps(list(product),cls=JsonCustomEncoder)
            series2=json.dumps(list(wifi_1m),cls=JsonCustomEncoder)
            series3=json.dumps(list(wifi_3m),cls=JsonCustomEncoder)
            series4=json.dumps(list(quantity),cls=JsonCustomEncoder)
            series5=json.dumps(list(satisfy),cls=JsonCustomEncoder)
            #[
                 #{sale_time_pro,sale_sum_pro,sale_sum_access},
                 #{sale_time_pro[1],sale_sum_pro[1],sale_sum_access[1]},
                 #{sale_time_pro[2],sale_sum_pro[2],sale_sum_access[2]}
                 #]
            #data1=json.dumps(series1,separators=(',',':'))
            data1=json.dumps(series1)
            print (data1)
            data2=json.dumps(series2)
            data3=json.dumps(series3)
            data4=json.dumps(series4)
            data5=json.dumps(series5)
            #return HttpResponse({'Series1':data1},content_type="application/json")
        
            return render(request,"index.html",
                {"all_region":all_region,
                #"all_province":all_province,
                "all_city": all_city,
                "region_id":region_id,
                "city_id":city_id,
                #"store_id":store.id,
                "select_store":select_store,
                "select_region":select_region,
                "select_city":select_city,
                "all_store": all_store,
                'Series1' : json.dumps(data1),
                'Series2' : json.dumps(data2),
                'Series3' : json.dumps(data3),
                'Series4' : json.dumps(data4),
                'Series5' : json.dumps(data5)
                #content_type="application/json",
                #"device_nums": device_count,
                #"actd_sum": dumps(sums),
                })
        else:
            print ("无权限")
            all_region = RegionDict.objects.all()
            return render(request,"index.html",{"all_region":all_region})
    def toDicts(objs):
        obj_arr=[]
        for o in objs:
                obj_arr.append(o.toDict())
        return obj_arr

'''
class Csv_ExportView(View):
    def get(self,request):
        resp="ok"
        return HttpResponse(json.dumps(resp), content_type="application/json")

    def post(self,request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        region_id=request.POST.get('Region_id',"")
        city_id=request.POST.get('City_id',"")
        store_id=request.POST.get('Store_id',"")
        day_select=request.POST.get('day_select',"")
        print (region_id)
        print (city_id)
        print (store_id)
        print (day_select)
        writer = csv.writer(response)
        writer.writerow(['First row', region_id, 'Bar', 'Baz'])
        writer.writerow(['Second row', city_id, 'B', 'C', '"Testing"', "Here's a quote"])
        writer.writerow(['Third row', store_id, 'B', 'C', '"Testing"', "Here's a quote"])
        writer.writerow(['Third row', day_select, 'B', 'C', '"Testing"', "Here's a quote"])
        return response
'''
def page_no_found(request):
    """
    全局404
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response("404.html", {})
    response.status_code = 404
    return response


def page_error(request):
    """
    全局500
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response("500.html", {})
    response.status_code = 500
    return response

# 测试用不安全sql注入
# class LoginUnsafeView(View):
#     def get(self, request):
#         return render(request, "login.html", {})
#     def post(self, request):
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#
#         import MySQLdb
#         conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='tp158917', db='mxonline2', charset='utf8')
#         cursor = conn.cursor()
#         sql_select = "select * from users_userprofile where email='{0}' and password='{1}'".format(user_name, pass_word)
#
#         result = cursor.execute(sql_select)
#         for row in cursor.fetchall():
#             # 查询到用户
#             pass
#         print 'mtianyan'
