# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acorndxData', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodclinicinfo',
            name='detectTime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bloodclinicinfo',
            name='lastChemotherapy',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bloodclinicinfo',
            name='takeTime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cancerclinicinfo',
            name='FFPE_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cancerclinicinfo',
            name='confirmedTime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cancerclinicinfo',
            name='detectTime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cancerclinicinfo',
            name='getBloodTime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cancerclinicinfo',
            name='newTissue_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cancerclinicinfo',
            name='operate_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detectinfo',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detectinfo',
            name='inspect_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detectinfo',
            name='receipt_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detectinfo',
            name='report_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detectinfo',
            name='send_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialrecord',
            name='cash_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialrecord',
            name='invoice_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialrecord',
            name='promotion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialrecord',
            name='u8_month',
            field=models.DateField(blank=True, null=True),
        ),
    ]
