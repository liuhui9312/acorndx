# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-28 07:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acorndxData', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='financialrecord',
            old_name='trade_receviable',
            new_name='trade_receivable',
        ),
    ]
