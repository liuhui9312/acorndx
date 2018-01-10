#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 13:47
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : dataStructureInitial.py
# @Software: PyCharm
import pandas as pd
from django.apps import apps
from django.contrib import admin
from acorndxData.models import DataStructure
from django.db import models, connection


def load_data():
    data_set = pd.read_csv('acorndxDatabase.txt', sep='\t')
    print(data_set.head())
    for i in list(data_set.index):
        tp = data_set.ix[i, :]
        cl = DataStructure()
        for j in list(data_set.columns):
            if j in ['readRight', 'writeRight']:
                setattr(cl, j, str(tp[j]))
            else:
                setattr(cl, j, tp[j])
        cl.save()


def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dict proxy error during model creation
        pass
    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)
    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)
    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}
    # Add in any fields that were provided
    if fields:
        attrs.update(fields)
    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)
    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)
    return model


def abstract_model():
    data_set = DataStructure.objects.all()
    data_set = [val.__dict__ for val in data_set]
    data_set = pd.DataFrame(data_set)
    # print(data_set.head())
    tables = list(set(data_set['belongTable']))
    new_models = {}
    for table in tables:
        table_items = data_set.ix[data_set['belongTable'] == table, :]
        fields = {}
        for r in list(table_items.index):
            item = table_items.ix[r, 'itemsEnglish']
            item_type = table_items.ix[r, 'itemsType']
            char_len = int(table_items.ix[r, 'itemsLength'])
            if item_type == 'char':
                fields[item] = models.CharField(max_length=char_len, null=True, blank=True)
            elif item_type == 'int':
                fields[item] = models.IntegerField(null=True, blank=True)
            elif item_type == 'float':
                fields[item] = models.FloatField(null=True, blank=True)
            elif item_type == 'date':
                fields[item] = models.DateField(null=True, blank=True)
        try:
            new_model = create_model(table,
                                     fields=fields,
                                     app_label='acorndxData',
                                     module='acorndxData.models')
            # print(new_model)
            new_models[table] = [new_model, fields]
        except Exception as e:
            print(e)
    return new_models


def create_or_upgrade():
    app_models = apps.get_app_config('acorndxData').get_models()
    exists_tables = {val.__doc__.split('(')[0]: [val, val.__doc__.split('(')[-1].replace(')', '').split(',')]
                     for val in app_models}
    print(exists_tables)
    new_models = abstract_model()
    for table in new_models.keys():
        if table not in exists_tables.keys():
            with connection.schema_editor() as schema_editor:
                # print(new_models[table])
                schema_editor.create_model(model=new_models[table][0])
                print('create new model {0}'.format(table))
        else:
            # 如果该表已经存在，则检查是否有新的表项加入
            print(exists_tables[table][1])
            new_items = [val for val in new_models[table][1].keys() if
                         val not in exists_tables[table][1]]
            if len(new_items):
                for item in new_items:
                    field = new_models[table][1][item]
                    with connection.schema_editor() as schema_editor:
                        # print(new_models[table])
                        schema_editor.add_field(new_models[table][0], field)
        # 删除和修改操作待开发
