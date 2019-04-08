# coding:utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


# null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
# blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填
# http://www.weiguda.com/blog/8/


class UserProfile(AbstractUser):
    # 昵称
    nick_name = models.CharField(
        max_length=50, verbose_name=u"昵称", default=u"")
    # 生日，可以为空
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    # 自定义的性别选择规则
    gender = models.CharField(max_length=10, choices=(
        ("male", "男"), ("female", "女")), default="female")
    # 地址
    address = models.CharField(max_length=100, default=u"")
    # 电话
    mobile = models.CharField(max_length=11, null=True, blank=True)
    # 头像 默认使用default.png
    image = models.ImageField(upload_to="image/%Y%m",
                              default=u"image/default.png", max_length=100)
    # 因为图像在后台存储的时候是一个字符串形式，所以需要设置一个max_length参数.
    # meta信息，即后台栏目名

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    # 获取用户未读消息的数量
    #def unread_nums(self):
    #    from operation.models import UserMessage
    #    return UserMessage.objects.filter(has_read=False, user=self.id).count()

    # 关于Meta：https://www.chenshaowen.com/blog/the-django-model-meta/
    # 重载Unicode方法，打印实例会打印username，username为继承自abstractuser
    def __str__(self):
        return self.username


# 邮箱验证码model
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    # 未设置null = true blank = true 默认不可为空
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(max_length=30, choices=(
        ("register", u"注册"), ("forget", u"找回密码"), ("updata_email", u"修改邮箱")),
        verbose_name=u"验证码类型")
    send_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"发送时间")
    # datetime.now():default时间为EmailVerifyRecord编译时间
    # datetime.now：default时间为EmailVerifyRecord实例化时间

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}[{1}]'.format(self.code, self.email)

'''
# 轮播图model
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(
        max_length=100, upload_to="banner/%Y/%m", verbose_name=u"轮播图")
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    # 默认index很大靠后。想要靠前修改index值。
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}(位于第{1}位)'.format(self.title, self.index)
'''
