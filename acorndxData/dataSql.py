#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 17:20
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : dataSql.py
# @Software: PyCharm
import pandas as pd
import datetime
# from django.contrib import auth
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from acorndxData.models import DetectInfo
from acorndxData.models import *
from acorndxData.configure import table_trans

table_dict = {'financial_record': FinancialRecord,
              'items_info': ItemsInfo,
              'person_info': PersonInfo,
              'sale_info': SaleInfo,
              'blood_info': BloodClinicInfo,
              'cancer_info': CancerClinicInfo,
              'blood_result': BloodResult,
              'cancer_result': CancerResult
              }


def update_or_create(table_name, tp_dict, context):
    # project 是数据表的基础类
    project = table_dict[table_name]
    p = project()
    try:
        if table_name == 'items_info':
            if not project.objects.filter(product_id=tp_dict['product_id']):
                context['create_num'] += 1
            else:
                p = project.objects.filter(product_id=tp_dict['product_id'])[0]
        elif table_name != 'items_info':
            if not project.objects.filter(sample_id=tp_dict['sample_id']):
                # print('创建')
                context['create_num'] += 1
            else:
                # print('更新')
                p = project.objects.filter(sample_id=tp_dict['sample_id'])[0]
        # print(project.__dict__)
        repeat = 1
        for title in tp_dict.keys():
            # 判断读取的记录和数据库中的是否有差异
            # setattr 设定类的属性值
            if p.__dict__[title] != tp_dict[title] and tp_dict[title] != 'nan':
                setattr(p, title, tp_dict[title])
            else:
                repeat += 1
        p.save()
        if len(list(tp_dict.keys())) == repeat:
            context['repeat'] += 1
    except Exception as e:
        context['error_num'] += 1
        if 'sample_id' in tp_dict.keys():
            context['error_log'].append('{}数据更新失败！'.format(tp_dict['sample_id']))
        else:
            context['error_log'].append('{}数据更新失败！'.format(tp_dict['product_id']))
        print(str(e))
    finally:
        del p


def get_all_data(project):
    # 查询project所有的数据
    context = {}
    if project in table_dict.keys():
        table_name = project
        project = table_dict[project]
        data_all = project.objects.all()
        if len(data_all) != 0:
            context['datas'] = []
            for tp_data in data_all:
                tp_data = tp_data.__dict__
                if 'heads' not in context.keys():
                    context['heads'] = [val for val in tp_data.keys() if not val.startswith('_') and val != 'id']
                    try:
                        context['heads_ch'] = [table_trans[table_name][val] for
                                               val in context['heads']]
                    except Exception as e:
                        print(e)
                context['datas'].append([tp_data[val]
                                         if not isinstance(tp_data[val],
                                                           datetime.date)
                                         else str(tp_data[val])
                                         for val in context['heads']])
        return context


def reverse(table, value):
    key = ''
    for key in table_trans[table].keys():
        if table_trans[table][key] == value:
            break
    if key != '':
        return key
    else:
        return None


def upload_data(file_path, project, context):
    if project in table_dict.keys():
        table_name = project
        # project = table_dict[project]
        try:
            table_data = pd.read_excel(file_path)
            # print(type(project))
            my_data = []
            total_num = 0
            for i in list(table_data.index):
                tp_dict = {}
                total_num += 1
                # 将表中的中文表头转换成对应的英文数据库表头，
                # 如果不在转换的字典中，则该列数据不能存储到数据库中；
                # 要去掉表格中表头的空格，否则匹配不上
                for j in range(len(list(table_data.columns))):
                    title = list(table_data.columns)[j].replace(' ', '')
                    title = reverse(table_name, title)
                    if title:
                        if 'date' not in title:
                            tp_dict[title] = str(table_data.ix[i, j])
                        else:
                            tp_dict[title] = str(table_data.ix[i, j]).split(' ')[0]
                if len(tp_dict) < len(table_trans[table_name]) / 2:
                    # 如果要更新的数据属性数量少于对应表的属性一半数量
                    # 中断更新
                    context['file_error'] = True
                    return context
                try:
                    update_or_create(table_name=table_name,
                                     tp_dict=tp_dict,
                                     context=context)
                except Exception as e:
                    print(e)
                my_data.append(tp_dict)
            context['total_num'] = total_num
        except Exception as e:
            print(e)
            context['file_error'] = True
        return context


def get_xy(xlab, ylab, data, group_by, groups):
    x_index = list(set(data[xlab]))
    values = []
    # 目前分组主要是按照时间来(按年,按月)
    if group_by == '':
        for x in x_index:
            tp = list(data.ix[data.ix[:, xlab] == x, ylab])
            if len(tp) > 0:
                if tp[0].isdigit():
                    values.append(sum([float(val) for val in tp]))
                else:
                    values.append([tp.count(val) for val in tp])
        new_set = pd.DataFrame({'index': x_index, ylab: values})
        return new_set
    else:
        if group_by == 'month':
            data['receipt_date'] = ['{0}/{1}'.format(val[0], val[1]) for val in groups]
        else:
            data['receipt_date'] = [str(val[0]) for val in groups]
        groups = list(set(data['receipt_date']))
        values = {val: [] for val in groups}
        for g in groups:
            for x in x_index:
                # 以收样日期作为分组
                tp = list(data[ylab][(data['receipt_date'] == g) & (data[xlab] == x)])
                if len(tp):
                    if tp[0].isdigit():
                        values[g].append(sum([float(val) for val in tp]))
                    else:
                        values[g].append(tp.count(val) for val in tp)
                else:
                    values[g].append(0)
        new_set = values.copy()
        new_set['index'] = x_index
        new_set = pd.DataFrame(new_set)
        # new_set.sort_values(by=)
        return new_set


def get_plot_data(context):
    table = context['table']
    # print(table)
    if context['group'] == '--':
        project = table_dict[table]
        data = project.objects.all()
        # 将数据库中的数据转化成DataFrame形式
        pd_data = []
        for dt in data:
            pd_data.append(dt.__dict__)
        pd_data = pd.DataFrame(pd_data)
        context['data_set'] = get_xy(xlab=context['x_label'], ylab=context['y_label'],
                                     data=pd_data, group_by='', groups=[])
        # 将统计项的标题由数据库表头改成中文表头
        cols = list(context['data_set'].columns)
        for i in list(range(len(cols))):
            if cols[i] in context['table_dict'].keys():
                cols[i] = context['table_dict'][cols[i]]
        context['data_set'].columns = cols
    return context


def get_statistic_data():
    data1 = FinancialRecord.objects.all()
    data2 = PersonInfo.objects.all()
    data3 = SaleInfo.objects.all()
    data_set = {}
    # 将数据库中的数据转化成DataFrame形式
    data1 = [val.__dict__ for val in data1]
    data2 = [val.__dict__ for val in data2]
    data3 = [val.__dict__ for val in data3]
    data1 = pd.DataFrame(data1)
    data2 = pd.DataFrame(data2)
    data3 = pd.DataFrame(data3)
    fin_data = pd.merge(data1, data2, on=['sample_id'])
    fin_data = pd.merge(fin_data, data3, on=['sample_id'])
    groups = [(val.year, val.month) for val in fin_data['receipt_date']]
    try:
        data_set['各城市按月销量统计'] = get_xy(xlab='cities', ylab='sale_price',
                                       data=fin_data, group_by='month', groups=groups)
        data_set['各城市按年销量统计'] = get_xy(xlab='cities', ylab='sale_price',
                                       data=fin_data, group_by='year', groups=groups)
        data_set['各代表按月销量统计'] = get_xy(xlab='market_represent', ylab='sale_price',
                                       data=fin_data, group_by='month', groups=groups)
        data_set['各代表按年销量统计'] = get_xy(xlab='market_represent', ylab='sale_price',
                                       data=fin_data, group_by='year', groups=groups)
        data_set['各套餐按年销量统计'] = get_xy(xlab='detect_content', ylab='sale_price',
                                       data=fin_data, group_by='year', groups=groups)
        data_set['各套餐按月销量统计'] = get_xy(xlab='detect_content', ylab='sale_price',
                                       data=fin_data, group_by='month', groups=groups)
    except Exception as e:
        print(e)
    return data_set
