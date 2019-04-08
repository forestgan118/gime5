#/usr/bin/python
# coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/10'

# 引入Django表单
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()