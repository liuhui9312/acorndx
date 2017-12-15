#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/30 15:04
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : configure.py
# @Software: PyCharm
YES_OR_NO = (
        ('YES', '是'),
        ('NO', '否'),
    )

products = (
    ('1', '肺癌LONGLUNG'),
    ('2', '全外显子检测'),
    ('3', '肺癌230基因'),
    ('4', '肺癌10基因'),
    ('5', '结直肠癌9基因'),
    ('6', '全癌种230基因'),
    ('7', '乳腺癌/卵巢癌BRCA1/2基因'),
    ('8', '乳腺癌21基因'),
    ('9', '血液病基因检测'),
    ('10', '急性髓细胞白血病(AML)76基因检测'),
    ('11', '血液病化疗药物临床获益基因检测'),
    ('12', '骨髓增生异常综合症(MDS)60基因检测'),
    ('13', '急性淋巴细胞白血病(ALL)基因检测'),
    ('14', '骨髓增殖性肿瘤(MPN)基因检测'),
)

table_trans = {'person_info': {'sample_id': '样本编号',
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
               'detect_info': {'sample_id': '样本编号',
                               'receipt_date': '接收日期',
                               'inspect_date': '送检日期',
                               'deadline': '应出报告日期',
                               'report_date': '出报告日期',
                               'send_date': '报告寄送日期',
                               'is_scientific': '是否是科研项目',
                               'detect_content': '检测内容'},
               'financial_record': {'sample_id': '样本编号',
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
                                    'is_receipt': '确认收款',
                                    'SP': 'SP'},
               'items_info': {'product_id': '产品编号',
                              'project_type': '项目分类',
                              'detect_content': '检测内容',
                              'detect_items': '检测项目'},
               'sale_info': {'sample_id': '样本编号',
                             'cities': '城市',
                             'areas': '地区',
                             'market_represent': '销售代表',
                             'submit_hospital': '送检医院',
                             'departments': '科室',
                             'station': '岗位',
                             'in_charge': '责任人',
                             'DSM': 'DSM',
                             'sale_price': '销售价格',
                             'agency_direct': '代理商/直营'}
               }
