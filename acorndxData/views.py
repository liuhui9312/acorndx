# coding=utf-8
import glob
import json
import codecs
import random
import string
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from acorndx.form import UserForm
from django.views.decorators.csrf import csrf_exempt
from acorndxData.dataSql import *
from acorndxData.dataPlot import *
from acorndxData.models import *
from pyecharts.constants import DEFAULT_HOST
from django.contrib.auth.decorators import login_required
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
    if req.user != '':
        context['user'] = req.user
        context['departments'] = get_department(account=req.user)
    else:
        context['user'] = None
        context['departments'] = get_department()
    return render(req, './acorndx/index.html', context)


@login_required(login_url='login')
def depart_view(request, depart):
    context = {}
    if request.method == 'GET' and request.user != '':
        context['departments'] = get_department(account=request.user)
        context['Departs'] = depart
        if depart == 'bioinfo':
            return render(request, 'acorndx/includes/analyst.html', context)
        else:
            # 根据访问的部门展示该部门能看到的数据项
            try:
                data_sets, data_items, en_ch = get_all_data(depart)
                # print(data_sets)
                context['data_items'] = sorted(data_items)
                file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                json_file = './acorndxData/static/json/{0}.json'.format(file_name)
                # print(json_file)
                # 定时清空临时文件
                if len(os.listdir('./acorndxData/static/json')) > 10:
                    for jsf in glob.glob('./acorndxData/static/json/*.json'):
                        os.remove(jsf)
                if not os.path.exists(json_file):
                    fi = codecs.open(json_file, 'w', 'utf-8')
                    json.dump(data_sets, fi, ensure_ascii=False)
                    fi.close()
                context['json_url'] = json_file.split('/')[-1]
                # if len(context['dataSets']):
            except Exception as e:
                print(e)
            return render(request, 'acorndx/includes/departView.html', context)


def load_data(request):
    context = {}
    try:
        context['departments'] = get_department(account=request.user)
        context['modify_tables'] = get_wr_table(account=request.user, choice='w')
        context['create_num'] = 0
        context['upgrade'] = 0
        context['repeat'] = 0
        context['total_num'] = 0
        context['error_num'] = 0
        context['error_log'] = []
        context['file_error'] = False
        context['state'] = -1
        if request.method == 'POST' and request.user != '':
            context['modify'] = request.POST.get('modify')
            print(context['modify_tables'])
            print(context['modify'])
            my_data = request.FILES.get('file_name', None)
            table_dir = './acorndxData/upload/{0}'.format(context['modify'])
            if my_data:
                # 如果上传的数据不为空，将数据存到服务器中
                file_name = my_data.__dict__['_name']
                if not os.path.exists(table_dir):
                    os.makedirs(table_dir)
                file_path = '{0}/{1}'.format(table_dir, file_name)
                fo = open(file_path, 'wb')
                fo.write(my_data.read())
                fo.close()
                # 开始进行数据库更新
                upload_data(file_path=file_path,
                            modify_table=context['modify'],
                            context=context)
                if context['error_num'] == 0:
                    context['state'] = 1
                context['upgrade'] = context['total_num']-context['repeat']-context['error_num']-context['create_num']
            else:
                context['file_error'] = True
    except Exception as e:
        print(e)
    finally:
        return render(request, 'acorndx/includes/uploadData.html', context)


@login_required(login_url='login')
def statistic_view(request, depart):
    context = {}
    if request.user != '':
        context['Departs'] = depart
        context['departments'] = get_department(account=request.user)
        data_sets, context['data_items'], en_ch = get_all_data(depart)
        data_sets = pd.DataFrame(data_sets)
        # print(context['data_sets'])
        if request.method == 'POST' and request.user != '':
            # 根据表单数据进行筛选
            x_label = request.POST.get('x_label')
            y_label = request.POST.get('y_label')
            group = request.POST.get('group')
            pic_type = request.POST.get('pic_type')
            is_sorted = request.POST.get('isSorted')
            time_line = request.POST.get('timeLine')
            context['script_list'] = []
            context['summary'] = request.POST.get('summary')
            context['statistic'] = request.POST.get('statistic')
            context['host'] = DEFAULT_HOST
            if not context['summary']:
                plot_data = get_xy(xlab=x_label,
                                   ylab=y_label,
                                   timeLine=time_line,
                                   group=group,
                                   data=data_sets)
                plot_data = pd.DataFrame(plot_data)
                print(plot_data)
                plot = Plot()
                context['Echarts'] = plot.chart_plot(dat=plot_data,
                                                     sort=is_sorted,
                                                     time_line=time_line,
                                                     group=group,
                                                     pic_type=pic_type)
                context['script_list'] = plot.script_list
                # print(context['Echarts'])
        return render(request, 'acorndx/includes/statistic.html', context)

