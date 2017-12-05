from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from acorndx.form import UserForm
from django.views.decorators.csrf import csrf_exempt
from acorndxData.dataSql import *
from django.core.paginator import Paginator
# Create your views here.
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。


# 注册
@csrf_exempt
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            # 获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            # 判断用户是否存在
            user = auth.authenticate(username=username,
                                     password=password,
                                     email=email)
            if user:
                context['userExit'] = True
                # return render(req, 'register.html', context)
                return HttpResponse('用户存在')
            if password != password2:
                return HttpResponse('两次输入密码不一致！')
            # 添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
            user.save()

            # 添加到session
            req.session['username'] = username
            # 调用auth登录
            auth.login(req, user)
            # 跳转到操作成功通知页面
            context['operation'] = '注册'
            return render(req, 'acorndx/success.html', context)
    else:
        context = {'isLogin': False}
    # 将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return render(req, './acorndx/register.html', context)


# 登陆
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
                return render(req, 'acorndx/success.html', context)
        else:
            # 比较失败，还在login
            # context = {'isLogin': False, 'pawd': False}
            # return render(req, 'login.html', context)
            return HttpResponse('账号或者密码错误')
    else:
        context = {'isLogin': False, 'pswd': True}
    return render(req, './acorndx/login.html', context)


# 登出
def logout_view(req):
    # 清理cookie里保存username
    auth.logout(req)
    return redirect('/')


def index_view(req):
    return render(req, './acorndx/index.html')


def data_view(request, table):
    if request.method == 'POST':
        # db_table = 'person_info'
        context = get_all_data(project=table)
        context['table'] = table
        # print(table)
        if context:
            context['hasData'] = True
        else:
            context['hasData'] = False
        if 'detail' in request.POST:
            return render(request, 'acorndx/includes/printData.html', context)
        elif table == 'financial_record':
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
        context['Departs'] = depart
        return render(request, 'acorndx/includes/departView.html', context)

    if request.method == 'POST':
        context['Departs'] = depart
        if 'comeback' in request.POST:
            return render(request, 'acorndx/includes/departView.html', context)


def statistic_view(request, depart):
    context = {}
    if request.method == 'POST':
        try:
            print('statistic')
            context['table'] = depart
            context['op'] = request.POST.get('my_method')
            context['area'] = request.POST.get('area')
            context['city'] = request.POST.get('city')
            context['date'] = request.POST.get('date')
            context['count'] = request.POST.get('count')
            context['product'] = request.POST.get('product')
            context['hospital'] = request.POST.get('hospital')
            context['team'] = request.POST.get('team')
            context['represent'] = request.POST.get('represent')
        except Exception as e:
            print(e)
        return render(request, 'acorndx/includes/plotData.html', context)

