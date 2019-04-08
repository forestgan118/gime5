#　models.py
from __future__ import unicode_literals
from django.db import models
#from users.models import UserProfile
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.exceptions import ValidationError
#from django.contrib.auth.models import User
#AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
class Menu(models.Model):
    '''页面中的菜单名'''
    caption = models.CharField(max_length=32)
    # django admin后台显示用
    class Meta:
        verbose_name_plural = "菜单表"
    # 重写__str__方法，实例化后的对象将以字符串的形式展示，但实际是一个obj,所以，请不要相信你的眼睛，必要时使用type(arg)进行验证
    def __str__(self):
        return self.caption


class Group(models.Model):
    '''权限url所属的权限组'''
    title = models.CharField(verbose_name='组名称',max_length=32)
    menu =models.ForeignKey(verbose_name='关联的菜单',to='Menu',default=1)  # 组所在的菜单

    class Meta:
        verbose_name_plural = '权限组'

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名',max_length=32)
    #name = models.OneToOneField(User)
    password = models.CharField(verbose_name='密码',max_length=256)
    email = models.CharField(verbose_name='邮箱',max_length=32)
    roles = models.ManyToManyField(verbose_name='用户关联的角色',to="Role",blank=True)
    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.name

class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32,verbose_name="角色名称")
    permissions = models.ManyToManyField(verbose_name='角色关联的权限',to='Permission',blank=True)
    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题',max_length=32)
    url = models.CharField(verbose_name="含正则URL",max_length=128)
    is_menu = models.BooleanField(verbose_name="是否是菜单")
    # menu_gp为null说明是title为菜单项
    menu_gp = models.ForeignKey(to="Permission", null=True, blank=True, verbose_name="组内菜单", related_name="pm")
    code = models.CharField(max_length=16, verbose_name="权限码")
    group = models.ForeignKey(to="Group", blank=True, verbose_name="所属组")



    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.title

