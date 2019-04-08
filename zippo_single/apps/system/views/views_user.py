#-*-coding:utf-8-*-  
from django.shortcuts import render  
from django.http import JsonResponse, HttpResponse  
from apps.system.services import userService  
from apps.system.models import User  
  
def user_login(request):  
    ''''' 
    用户登录 
    :param request: 
    :return: 
    '''  
    if request.method == "GET":  
        return render(request, "login.html")  
    else:  
        res = {}  
        username = request.POST.get("username")  
        password = request.POST.get("password")  
        user = User.objects.filter(username=username, password=password).first()  
        if not user:  
            res["status"]= "false"  
        else:  
            userService.init_user_permission(request, user)  
        return JsonResponse(res)  