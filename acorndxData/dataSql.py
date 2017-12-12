#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 17:20
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : dataSql.py
# @Software: PyCharm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from acorndxData.models import DetectInfo
from acorndxData.models import FinancialRecord
from acorndxData.models import ItemsInfo
from acorndxData.models import PersonInfo
from acorndxData.models import SaleInfo
import json
table_dict = {'detect_info': DetectInfo,
              'financial_record': FinancialRecord,
              'items_info': ItemsInfo,
              'person_info': PersonInfo,
              'sale_info': SaleInfo}
table_trans = {'person_info': {'id': '系统ID',
                               'sample_id': '样本编号',
                               'sample_nation': '民族',
                               'sample_age': '年龄',
                               'certificate_type': '证件类型',
                               'certificate_id': '身份证号',
                               'sample_name': '患者姓名',
                               'contact_phone': '联系电话',
                               'contact_email': '电子邮箱',
                               'contact_address': '通讯地址',
                               'submit_physician': '送检医生',
                               'physician_phone': '医师电话',
                               'medical_record_id': '病历号'},
               'detect_info': {'id': '系统ID',
                               'sample_id': '样本编号',
                               'receipt_date': '接收日期',
                               'inspect_date': '送检日期',
                               'deadline': '应出报告日期',
                               'report_date': '出报告日期',
                               'send_date': '报告寄送日期',
                               'is_scientific': '是否是科研项目',
                               'detect_content_id': '检测内容ID'},
               'financial_record': {'id': '系统ID',
                                    'sample_id': '样本编号',
                                    'serial_number': '流水号',
                                    'sale_price': '销售价格',
                                    'is_charge': '是否收费',
                                    'invoice_id': '发票号',
                                    'invoice_company': '开票单位',
                                    'invoice_date': '开票日期',
                                    'invoice_amount': '开票金额',
                                    'receipt_id': '收据号',
                                    'receivable_way': '回款方式',
                                    'bank_charges': '银行手续费',
                                    'trade_receivable': '应收货款',
                                    'actual_payment': '实际货款',
                                    'settlement_price': '结算底价',
                                    'cash_date': '回款日期',
                                    'cash_month': '回款月',
                                    'voucher_id': '用友凭证号',
                                    'promotion_expenses': '推广费支付金额',
                                    'promotion_date': '推广费支付日期',
                                    'u8_month': 'U8确认收入月份',
                                    'is_receipt': '确认收款'},
               'items_info': {'id': '系统ID',
                              'project_type': '项目分类',
                              'detect_content': '检测内容',
                              'detect_items': '检测项目'},
               'sale_info': {'id': '系统ID',
                             'sample_id': '样本编号',
                             'citys': '城市',
                             'areas': '地区',
                             'market_represent': '销售代表',
                             'submit_hosptial': '送检医院',
                             'departments': '科室',
                             'station': '岗位',
                             'in_charge': '责任人',
                             'DSM': 'DSM',
                             'sale_price': '销售价格',
                             'agency_direct': '代理商/直营'}
               }


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
