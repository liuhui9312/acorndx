# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acorndxData', '0004_financialrecord_receivable_way'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialrecord',
            name='voucher_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]