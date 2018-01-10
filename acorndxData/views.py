import os
import json
import codecs
import csv
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from acorndx.form import UserForm
from django.views.decorators.csrf import csrf_exempt
from acorndxData.dataSql import *
from acorndxData.models import *
# Create your views here.
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。


@csrf_exempt
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        context['userExit'] = False
        context['accountRepeat'] = False
        context['passwordError'] = False
        context['formError'] = False
        context['accountError'] = False
        if form.is_valid():
            # 获得表单数据
            chinese_name = form.cleaned_data['chineseName']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if len(UserInfo.objects.filter(userName=chinese_name)) == 0:
                context['accountError'] = True
            else:
                if len(User.objects.filter(username=username)):
                    context['accountRepeat'] = True
                else:
                    user = auth.authenticate(username=username,
                                             password=password,
                                             email=email)
                    if user:
                        context['userExit'] = True
                    if password != password2:
                        context['passwordError'] = True
                    # 添加到数据库（还可以加一些字段的处理）
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email)
                    # 将注册的用户账号更新到Userinfo表
                    my_user = UserInfo.objects.filter(userName=chinese_name)
                    if len(my_user) == 1:
                        my_user = my_user[0]
                        my_user.account = username
                        # 默认只有本部门的读写权限
                        my_user.userRight = str(my_user.userDepartmentId_id)
                        my_user.save()
                        print('更新用户的注册信息')
                    user.save()
                    # 添加到session
                    req.session['username'] = username
                    # 调用auth登录
                    auth.login(req, user)
                    context['operation'] = '注册'
            context['departments'] = get_department()
            return render(req, './acorndx/registerState.html', context)
        else:
            context['formError'] = True
    else:
        context['departments'] = get_department()
        return render(req, './acorndx/register.html', context)


@csrf_exempt
def login_view(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        # 获取的表单数据与数据库进行比较
        context = {}
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # 比较成功，跳转index
                auth.login(req, user)
                req.session['username'] = username
                # return redirect('/')
                context['operation'] = '登陆'
                context['departments'] = get_department(account=username)
                return render(req, 'acorndx/registerState.html', context)
        else:
            # 比较失败，还在login
            return HttpResponse('账号或者密码错误')
    else:
        context = {'isLogin': False, 'pswd': True}
    context['departments'] = get_department()
    return render(req, './acorndx/login.html', context)


def logout_view(req):
    # 清理cookie里保存username
    auth.logout(req)
    return redirect('/')


def index_view(req):
    context = {}
    if True:
        context['departments'] = get_department()
        return render(req, './acorndx/index.html', context)


def data_view(request, table):
    context = {}
    if request.method == 'POST':
        # context = get_all_data(project=table)
        context['table'] = table
        # print(table)
        if context:
            context['hasData'] = True
        else:
            context['hasData'] = False
        context['departments'] = get_department()
        if 'detail' in request.POST:
            # print(context['heads_ch'])
            return render(request, 'acorndx/includes/printData.html', context)
        elif table == 'financial_record':
            context['table_dict'] = table_trans[table]
            return render(request, 'acorndx/includes/financial.html', context)
        elif table == 'person_info':
            return render(request, 'acorndx/includes/person.html', context)
        elif table == 'sale_info':
            return render(request, 'acorndx/includes/sale.html', context)
        else:
            return HttpResponse('还在开发当中，敬请期待')


def depart_view(request, depart):
    context = {}
    if request.method == 'GET':
        context['departments'] = get_department()
        context['Departs'] = depart
        if depart == 'analyst':
            return render(request, 'acorndx/includes/analyst.html', context)
        else:
            return render(request, 'acorndx/includes/departView.html', context)

    if request.method == 'POST':
        context['departments'] = get_department()
        context['Departs'] = depart
        if 'comeback' in request.POST and depart != 'analyst':
            return render(request, 'acorndx/includes/departView.html', context)
        elif 'comeback' in request.POST and depart == 'analyst':
            return render(request, 'acorndx/includes/analyst.html', context)


