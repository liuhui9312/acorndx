#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/20 10:25
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : form.py
# @Software: PyCharm
from acorndxData.configure import *
from django import forms
count_by = (
    ('1', '样本编号'),
    ('2', '销售价格'),
)


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
    email = forms.EmailField()


class ChoiceForm(forms.Form):
    areas = forms.CharField(max_length=5)
    cities = forms.CharField(max_length=15)
    statistic = forms.IntegerField(widget=forms.Select(choices=count_by))
    product = forms.IntegerField(widget=forms.Select(choices=products))
