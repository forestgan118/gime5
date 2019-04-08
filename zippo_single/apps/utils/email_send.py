# /usr/bin/python
# coding:utf-8


from random import Random
# 导入Django自带的邮件模块
from django.core.mail import send_mail, EmailMessage

from users.models import EmailVerifyRecord
# 导入setting中发送邮件的配置
from zippo_single.settings import EMAIL_FROM
# 发送html格式的邮件:
from django.template import loader
# def random_str(randomlength=8):
#     '''
#     生成随机字符串
#     '''
#     str = ''
#     chars = 'AaBbCcDdEeFfGgHhJjIi234567890'
#     length = len(chars)-1
#     print length
#     random = Random
#     for i in range(randomlength):
#         str+=chars[random.randint(0,length)]
#     return str

# 生成随机字符串


def random_str(randomlength=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_register_email(email, send_type="register"):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_recod = EmailVerifyRecord()
    # 生成随机的code放入链接
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_recod.code = code
    # print ( "send email" )
    email_recod.email = email
    email_recod.send_type = send_type
    email_recod.save()
    #print(code)

    # 定义邮件内容:
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "上海品感广告有限公司注册激活链接"
        email_body = "请点击激活：http://120.78.188.123:8000/active/{0}".format(code)
        '''
        email_body = loader.render_to_string(
            "email_register.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }
        )

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
        '''
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("注册激活邮件发送成功！")
    elif send_type == "forget":
        email_title = "上海品感广告有限公司 找回密码链接"
        email_body = "请点击激活：http://120.78.188.123:8000/reset/{0}/".format(code)
        '''
        email_body = loader.render_to_string(
            "email_forget.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }

        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
        '''
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("找回密码邮件发送成功！")
    elif send_type == "update_email":
        email_title == "邮箱修改验证码"
        email_body = "你的邮箱验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body,
                                EMAIL_FROM, [email])
        if send_status:
            print("修改邮箱验证码邮件发送成功！")


'''
        email_title = "mtianyan慕课小站 修改邮箱验证码"
        email_body = loader.render_to_string(
            "email_update_email.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }
        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
'''
