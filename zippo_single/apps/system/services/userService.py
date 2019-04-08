from ..models import Menu  
  
def init_user_permission(request, user):  
    ''''' 
    查询出用户的所有权限，进行分类写入session进行保存 
    :param request: 
    :param user: 
    :return: 
    '''  
    # 查询出用户的所有权限  
    permisson_item_list = user.roles.values('permissons__title',  
                                            'permissons__url',  
                                            'permissons__menu_id'  
                                            ).distinct()  
    permisson_url_list = []  
    permisson_menu_list = []  
    all_menu_list = list(Menu.objects.values("id", "title", "parent_id"))  
    for permission_item in permisson_item_list:  
        permisson_url_list.append(permission_item["permissons__url"])  
        if permission_item["permissons__menu__id"]:  
            temp = {  
                "title": permission_item["permissons__title"],  
                "url": permission_item["permissons__url"],  
                "menu_id": permission_item["permissons__menu_id"]  
            }  
            permisson_menu_list.append(temp)  
    # 写入session  
    from django.conf import settings  
    request.session[settings.SESSION_PERMISSION_URL_KEY] = permisson_url_list  
    request.session[settings.SESSION_MENU_KEY] = {  
        settings.MENU_ALL: all_menu_list,  
        settings.MENU_PERMISSON: permisson_menu_list,  
    }