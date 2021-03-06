import os
import json
import codecs
import csv
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from acorndx.form import UserForm
from django.views.decorators.csrf import csrf_exempt
from acorndxData.dataSql import *
from pyecharts.constants import DEFAULT_HOST
from acorndxData.dataPlot import *
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
        context = get_all_data(project=table)
        context['table'] = table
        # print(table)
        if context:
            context['hasData'] = True
        else:
            context['hasData'] = False
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
        context['Departs'] = depart
        if depart == 'analyst':
            return render(request, 'acorndx/includes/analyst.html', context)
        else:
            return render(request, 'acorndx/includes/departView.html', context)

    if request.method == 'POST':
        context['Departs'] = depart
        if 'comeback' in request.POST and depart != 'analyst':
            return render(request, 'acorndx/includes/departView.html', context)
        elif 'comeback' in request.POST and depart == 'analyst':
            return render(request, 'acorndx/includes/analyst.html', context)


def statistic_view(request, depart):
    # 获取统计结果需要的的各项筛选条件
    context = {}
    if request.method == 'POST':
        context['table'] = depart
        context['x_label'] = request.POST.get('x_label')
        context['y_label'] = request.POST.get('y_label')
        context['group'] = request.POST.get('group')
        context['pic_type'] = request.POST.get('pic_type')
        context['table_dict'] = table_trans[depart]
        context['summary'] = request.POST.get('summary')
        context['isSorted'] = request.POST.get('isSorted')
        context['data_set'] = {}
        context['host'] = DEFAULT_HOST
        context['script_list'] = []
        if not context['summary']:
            try:
                # 先从数据库中获取用于统计作图的数据
                context = get_plot_data(context)
                # 根据作图的类型获取统计图对象
                if context['pic_type'] == 'Bar':
                    this_plot = PlotBar()
                    context['echarts'] = this_plot.bar_plot(dat=context['data_set'],
                                                            sort=context['isSorted'])
                    context['script_list'] = this_plot.script_list
                elif context['pic_type'] == 'Pie':
                    this_plot = PlotPie()
                    context['echarts'] = this_plot.plot_pie(dat=context['data_set'],
                                                            sort=context['isSorted'])
                    context['script_list'] = this_plot.script_list
                elif context['pic_type'] == 'Line':
                    this_plot = PlotLine()
                    context['echarts'] = this_plot.plot_line(dat=context['data_set'],
                                                             sort=context['isSorted'])
            except Exception as e:
                print(e)
        else:
            try:
                # 先从数据库中获取用于统计作图的数据
                context['data_set'] = get_statistic_data()
                this_plot = MultiPlot()
                context['script_list'] = this_plot.script_list
                context['echarts'] = this_plot.multi_plot(context['data_set'])
            except Exception as e:
                print(e)
        return render(request, 'acorndx/includes/plotData.html', context)


def load_data(request, table):
    context = {}
    if request.method == 'POST':
        context['table'] = table
        context['create_num'] = 0
        context['repeat'] = 0
        context['total_num'] = 0
        context['error_num'] = 0
        context['error_log'] = []
        context['file_error'] = False
        table_dir = './acorndxData/upload/{0}'.format(table)
        context['download'] = True if request.POST.get('download') else False
        print(context['download'])
        my_data = request.FILES.get('file_name', None)
        if my_data and not context['download']:
            # 如果上传的数据不为空，将数据存到服务器中
            file_name = my_data.__dict__['_name']
            if not os.path.exists(table_dir):
                os.makedirs(table_dir)
            file_path = '{0}/{1}_{2}'.format(table_dir, len(os.listdir(table_dir)), file_name)
            fo = open(file_path, 'wb')
            fo.write(my_data.read())
            fo.close()
            # 开始进行数据库更新
            context = upload_data(file_path=file_path,
                                  project=table,
                                  context=context)
            context['update_num'] = context['total_num']-context['repeat']-context['error_num']-context['create_num']
            if context['error_num'] == 0:
                context['state'] = 1
            else:
                context['state'] = 0
            return render(request, 'acorndx/uploadState.html', context)
        elif not my_data and not context['download']:
            context['Departs'] = table
            return render(request, 'acorndx/includes/departView.html', context)
        elif context['download']:
            # download data
            context['Departs'] = table
            # get data
            return HttpResponse('未开发')


def get_data(request, depart):
    context = {}
    if request.method == "GET":
        this_table = table_dict[depart]
        limit = request.GET.get('limit')  # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        sort_column = request.GET.get('sort')  # which column need to sort
        order = request.GET.get('order')  # ascending or descending
        all_records = []
        if search:
            if sort_column in table_trans[this_table].keys():
                if order == 'desc':
                    sort_column = '-{}'.format(sort_column)
                all_records = this_table.objects.all().order_by(sort_column)
            all_records_count = all_records.count()
            if not offset:
                offset = 0
            if not limit:
                limit = 20
            my_page = Paginator(all_records, limit)
            page = int(int(offset) / int(limit)+1)
            context = {'total': all_records_count, 'rows': []}
            for tp in my_page.page(page):
                context['rows'].append()
        # 需要json处理下数据格式
        return HttpResponse(json.dumps(context))


def analyst_view(request, depart):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        context['title'] = request.POST.get('title')
        context['describe'] = request.POST.get('describe')
        context['email'] = request.POST.get('email')
        context['Departs'] = depart
        context['file_data'] = request.FILES.get('file_name', None)
        if context['file_data']:
            # 将上传得到的数据存储到服务器中，由后台进行操作处理
            context['file_name'] = context['file_data'].__dict__['_name']
            print(context['file_name'])
            # print(context['file_data'].read())
        context['executing_state'] = 'running'
        # 添加执行方法 run(context)
        return render(request, 'acorndx/includes/analystResult.html', context)


def output(request):
    response = HttpResponse(content_type='text/csv')
    # 导出xls文件
    # response['Content-Type'] = 'application/vnd.ms-excel;charset=UTF-8'
    response['Content-Disposition'] = 'attachment; filename=%s' % 'user.csv'
    objs = PersonInfo.objects.all()
    # 解决中文乱码的问题
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(['样本编号', '身份证号', '邮箱'])
    for o in objs:
        writer.writerow([o.sample_id, o.certificate_id, o.contact_email])
    return response
