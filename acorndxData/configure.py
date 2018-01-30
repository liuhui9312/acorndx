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

table_trans = {'FinancialRecord': '财务和销售数据',
               'PersonInfo': '患者基本信息',
               'CancerClinicInfo': '实体瘤患者基本病情与治疗史',
               'CancerResult': '实体瘤基因检测结果',
               'BloodClinicInfo': '血液病患者基本病情与检测治疗史',
               'BloodResult': '血液病基因检测结果',
               }
