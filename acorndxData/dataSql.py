#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 17:20
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : dataSql.py
# @Software: PyCharm
import pandas as pd
# from django.contrib import auth
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
from acorndxData.models import DetectInfo
from acorndxData.models import FinancialRecord
from acorndxData.models import ItemsInfo
from acorndxData.models import PersonInfo
from acorndxData.models import SaleInfo
from acorndxData.configure import table_trans

table_dict = {'detect_info': DetectInfo,
              'financial_record': FinancialRecord,
              'items_info': ItemsInfo,
              'person_info': PersonInfo,
              'sale_info': SaleInfo}


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
                        context['heads_ch'] = [table_trans[table_name][val] for val in context['heads']]
                    except Exception as e:
                        print(e)
                context['datas'].append([tp_data[val] for val in context['heads']])
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
