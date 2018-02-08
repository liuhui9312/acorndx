#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 17:20
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : dataSql.py
# @Software: PyCharm
import os
import pandas as pd
from django.apps import apps
from acorndxData.models import *
from acorndxData.configure import table_trans


def get_table_trans():
    # 获取业务数据库的表名的中英文对照表
    table_items = DataStructure.objects.all()
    table_items = {val.itemsChinese: val.itemsEnglish for val in table_items}
    return table_items


def get_table_class():
    # 获取业务数据库中各表的对象和各表包含的列名
    app_models = apps.get_app_config('acorndxData').get_models()
    # 需要注意上传数据中并不包含系统的ID
    table_dict = {val.__doc__.split('(')[0]: [val,
                                              val.__doc__.split('(')[-1].replace(')', '').split(',')]
                  for val in app_models}
    return table_dict


def get_department(account=''):
    departs = Department.objects.all()
    # 通过登录的账户信息以及UserInfo表获取该账户的身份信息
    # 通过身份信息获取其能看到的界面
    user = UserInfo.objects.filter(account=account)
    if user:
        user = user[0]
        user_items = list(user.userRight)
        # print(user_items)
        departs_dic = {val.department: val.departmentName
                       for val in departs if str(val.departmentId) in user_items}
        departs_dic = {val: departs_dic[val] for val in departs_dic.keys()}
    else:
        departs_dic = None
    return departs_dic


def get_wr_table(account='', choice='w'):
    table_set = DataStructure.objects.all()
    user = UserInfo.objects.filter(account=account)
    if user:
        user = user[0]
        user_depart = str(user.userDepartmentId_id)
        tables = []
        if choice == 'w':
            tables = [val.belongTable for val in table_set if user_depart in str(val.writeRight)]
            tables = list(set(tables))
        elif choice == 'r':
            tables = [val.belongTable for val in table_set if user_depart in str(val.readRight)]
            tables = list(set(tables))
        # print(write_tables)
        if len(tables):
            tables = {table_trans[key]: key for key in list(table_trans.keys())}
            return tables
    else:
        return None


def update_or_create(table_name, tp_dict, context):
    # project 是数据表的基础类
    table_dict = get_table_class()
    project = table_dict[table_name][0]
    p = project()
    try:
        if not project.objects.filter(sample_id=tp_dict['sample_id']):
            # print('创建')
            context['create_num'] += 1
        else:
            # print('更新')
            p = project.objects.filter(sample_id=tp_dict['sample_id'])[0]
        # print(project.__dict__)
        repeat = 0
        for title in tp_dict.keys():
            # 判断读取的记录和数据库中的是否有差异
            # setattr 设定类的属性值
            if title not in p.__dict__.keys():
                context['error_log'].append('warring {0} 不是选择上传的表中的字段'.format(title))
                continue
            if str(p.__dict__[title]) != str(tp_dict[title])\
                    and tp_dict[title] != 'nan':
                if isinstance(p.__dict__[title], float) or isinstance(p.__dict__[title], int):
                    if float(p.__dict__[title]) - float(tp_dict[title]) == 0:
                        repeat += 1
                        continue
                setattr(p, title, tp_dict[title])
                # print(p.__dict__[title], tp_dict[title])
            else:
                repeat += 1
        p.save()
        if len(list(tp_dict.keys())) == repeat:
            # repeat的大小和tp_dict的值完全一样，说明没有更新，完全一致的
            context['repeat'] += 1
    except Exception as e:
        context['error_num'] += 1
        if 'sample_id' in tp_dict.keys():
            context['error_log'].append('error:{}数据更新失败！'.format(tp_dict['sample_id']))
        print(str(e)+'\tat update_or_create')
    finally:
        del p


def upload_data(file_path, modify_table, context):
    table_dict = get_table_class()
    table_items = get_table_trans()
    if modify_table in table_dict.keys():
        table_name = modify_table
        # project = table_dict[project]
        try:
            table_data = pd.read_excel(file_path)
            # print(type(project))
            # my_data = []
            total_num = 0
            for i in list(table_data.index):
                tp_dict = {}
                total_num += 1
                # 将表中的中文表头转换成对应的英文数据库表头，
                # 如果不在转换的字典中，则该列数据不能存储到数据库中；
                # 要去掉表格中表头的空格，否则匹配不上
                for j in range(len(list(table_data.columns))):
                    title = list(table_data.columns)[j].replace(' ', '')
                    if title in table_items.keys():
                        title = table_items[title]
                    else:
                        context['error_log'].append('数据库中没有{0}字段，未能导入！'.format(title))
                    if title:
                        if 'date' not in title:
                            tp_dict[title] = str(table_data.ix[i, j])
                        else:
                            tp_dict[title] = str(table_data.ix[i, j]).split(' ')[0]
                if abs(len(tp_dict) + 1 - len(table_dict[table_name][1])) > 3:
                    # 如果要更新的数据表相差超过三个表项
                    # + 1 是因为数据表中无id这一系统自增表项
                    # 中断更新
                    context['file_error'] = True
                    return context
                update_or_create(table_name=table_name,
                                 tp_dict=tp_dict,
                                 context=context)
                # my_data.append(tp_dict)
            context['total_num'] = total_num
        except Exception as e:
            print(str(e)+'\tat upload_data')
            context['file_error'] = True
        finally:
            os.remove(file_path)
            print('remove {}'.format(file_path))
        return context


def get_all_data(depart):
    # 查询project所有的数据
    depart_id = []
    for p in Department.objects.filter(department=depart):
        depart_id.append(str(p.departmentId))
    # print('部门id-{0}'.format(depart_id[0]))
    read_sets = [(val.belongTable, val.itemsEnglish,
                  val.itemsChinese) for val in DataStructure.objects.all()
                 if depart_id[0] in str(val.readRight)]
    en_ch = {val[1]: val[2] for val in read_sets}
    read_tables = list(set([val[0] for val in read_sets]))
    table_dict = get_table_class()
    data_sets = {}
    data_items = []
    for table in read_tables:
        if table in table_dict.keys():
            data_sets[table] = []
            project = table_dict[table][0]
            p = project
            for val in p.objects.all().values():
                tp = {}
                for item in val.keys():
                    if item in en_ch.keys():
                        data_items.append(en_ch[item])
                        if '日期' in en_ch[item]:
                            tp[en_ch[item]] = str(val[item])
                        else:
                            tp[en_ch[item]] = val[item]
                data_sets[table].append(tp)
    data_sets = {val: data_sets[val] for val in data_sets.keys()
                 if len(data_sets[val])}
    data_items = list(set(data_items))
    # print(data_items)
    # print(len(data_items))
    new_dict = {}
    for k1, v1 in data_sets.items():
        for v in v1:
            if v['样本编号'] not in new_dict.keys():
                new_dict[v['样本编号']] = v.copy()
            else:
                new_dict[v['样本编号']].update(v)
    for k, v in new_dict.items():
        for v1 in data_items:
            if v1 not in v.keys():
                new_dict[k][v1] = ''
        # print(len(new_dict[k]))
    data_sets = list(new_dict.values())
    return data_sets, data_items, en_ch


def get_xy(xlab, ylab, timeLine, group, data):
    x_index = list(set(data[xlab]))
    values = {}
    if timeLine == '--':
        if group == '--':
            value = []
            for x in x_index:
                tp = list(data.ix[data[xlab] == x, ylab])
                if len(tp):
                    tp = ['0' if val == 'nan' else val for val in tp]
                    if isinstance(tp[0], int) or isinstance(tp[0], float) \
                            or tp[0].isdigit():
                        value.append(sum([float(val) for val in tp]))
                    else:
                        value.append(len(tp))
                else:
                    value.append(0)
            values[ylab] = value
        else:
            groups = list(set(data[group]))
            for g in groups:
                value = []
                for x in x_index:
                    tp = list(data.ix[(data[xlab] == x) & (data[group] == g),
                                      ylab])
                    if len(tp):
                        tp = ['0' if val == 'nan' else val for val in tp]
                        if isinstance(tp[0], int) or isinstance(tp[0], float) or \
                                tp[0].isdigit():
                            value.append(sum([float(val) for val in tp]))
                        else:
                            value.append(len(tp))
                    else:
                        value.append(0)
                values['{0}_{1}'.format(g, ylab)] = value
    else:
        if timeLine == 'month':
            data['送检日期'] = ['{0}/{1}'.format(val.split('-')[0],
                                             val.split('-')[1])
                            for val in data['送检日期']]
        elif timeLine == 'year':
            data['送检日期'] = ['{0}年'.format(val.split('-')[0]) for val in data['送检日期']]
        # print(data['送检日期'])
        time_groups = list(set(data['送检日期']))
        if group == '--':
            for t in time_groups:
                value = []
                for x in x_index:
                    tp = list(data[ylab][(data[xlab] == x) & (data['送检日期'] == t)])
                    if len(tp):
                        tp = ['0' if val == 'nan' else val for val in tp]
                        if isinstance(tp[0], int) or isinstance(tp[0], float) \
                                or tp[0].isdigit():
                            value.append(sum([float(val) for val in tp]))
                        else:
                            value.append(len(tp))
                    else:
                        value.append(0)
                values['{0}_{1}'.format(t, ylab)] = value
        else:
            groups = list(set(data[group]))
            for t in time_groups:
                for g in groups:
                    value = []
                    for x in x_index:
                        tp = list(data[ylab][(data[xlab] == x) &
                                             (data['送检日期'] == t) &
                                             (data[group] == g)])
                        if len(tp):
                            tp = ['0' if val == 'nan' else val for val in tp]
                            if isinstance(tp[0], int) or isinstance(tp[0], float) or tp[0].isdigit():
                                value.append(sum([float(val) for val in tp]))
                            else:
                                value.append(len(tp))
                        else:
                            value.append(0)
                    values['{0}_{1}_{2}'.format(t, g, ylab)] = value
    values['index'] = x_index
    # for k, v in values.items():
    #     print(k)
    #     print(v)
    return values
