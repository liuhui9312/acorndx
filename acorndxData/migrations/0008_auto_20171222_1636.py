# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-22 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acorndxData', '0007_auto_20171222_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saleinfo',
            old_name='deadline',
            new_name='dead_date',
        ),
    ]
