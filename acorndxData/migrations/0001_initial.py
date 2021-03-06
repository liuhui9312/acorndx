# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BloodClinicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('takeTime', models.DateField()),
                ('detectTime', models.DateField()),
                ('importantFeature', models.CharField(blank=True, max_length=30, null=True)),
                ('relevantHistory', models.CharField(blank=True, max_length=30, null=True)),
                ('chemotherapy', models.CharField(blank=True, max_length=20, null=True)),
                ('lastChemotherapy', models.DateField()),
                ('recentIMM', models.CharField(blank=True, max_length=20, null=True)),
                ('specificIMM', models.CharField(blank=True, max_length=20, null=True)),
                ('radiotherapy', models.CharField(blank=True, max_length=20, null=True)),
                ('marrow', models.CharField(blank=True, max_length=20, null=True)),
                ('WBC', models.CharField(blank=True, max_length=20, null=True)),
                ('RBC', models.CharField(blank=True, max_length=20, null=True)),
                ('Hb', models.CharField(blank=True, max_length=20, null=True)),
                ('PLT', models.CharField(blank=True, max_length=20, null=True)),
                ('primitiveCell', models.CharField(blank=True, max_length=20, null=True)),
                ('juvenileCell', models.CharField(blank=True, max_length=20, null=True)),
                ('otherCell', models.CharField(blank=True, max_length=20, null=True)),
                ('marrowResult', models.CharField(blank=True, max_length=30, null=True)),
                ('clinicalDiagnosis', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BloodResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('confirmDisease', models.CharField(blank=True, max_length=20, null=True)),
                ('confirmTime', models.CharField(blank=True, max_length=20, null=True)),
                ('remark', models.CharField(blank=True, max_length=20, null=True)),
                ('isPTD', models.CharField(blank=True, max_length=10, null=True)),
                ('isNegative', models.CharField(blank=True, max_length=10, null=True)),
                ('isMultiSite', models.CharField(blank=True, max_length=10, null=True)),
                ('geneNumber', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CancerClinicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('sampleType', models.CharField(blank=True, max_length=10, null=True)),
                ('sendTogether', models.CharField(blank=True, max_length=10, null=True)),
                ('tissueType', models.CharField(blank=True, max_length=10, null=True)),
                ('primaryOrMet', models.CharField(blank=True, max_length=10, null=True)),
                ('FFPE_date', models.DateField()),
                ('newTissue_date', models.DateField()),
                ('sampleSize', models.CharField(blank=True, max_length=10, null=True)),
                ('getBloodTime', models.DateField()),
                ('timeState', models.CharField(blank=True, max_length=10, null=True)),
                ('tissueTyping', models.CharField(blank=True, max_length=10, null=True)),
                ('clinicalDiagnosis', models.CharField(blank=True, max_length=20, null=True)),
                ('standardCD', models.CharField(blank=True, max_length=20, null=True)),
                ('confirmedTime', models.DateField()),
                ('stateT', models.CharField(blank=True, max_length=5, null=True)),
                ('stateN', models.CharField(blank=True, max_length=5, null=True)),
                ('stateM', models.CharField(blank=True, max_length=5, null=True)),
                ('clinicalStages', models.CharField(blank=True, max_length=10, null=True)),
                ('recur', models.CharField(blank=True, max_length=10, null=True)),
                ('transfer', models.CharField(blank=True, max_length=10, null=True)),
                ('met', models.CharField(blank=True, max_length=30, null=True)),
                ('ECOG', models.CharField(blank=True, max_length=20, null=True)),
                ('operate_record', models.CharField(blank=True, max_length=10, null=True)),
                ('operate_date', models.DateField()),
                ('radiotherapyRecord', models.CharField(blank=True, max_length=5, null=True)),
                ('radioInitiation', models.CharField(blank=True, max_length=30, null=True)),
                ('treatmentStage', models.CharField(blank=True, max_length=10, null=True)),
                ('chemotherapy', models.CharField(blank=True, max_length=10, null=True)),
                ('chemotherapyAndTime', models.CharField(blank=True, max_length=100, null=True)),
                ('targetMedicine', models.CharField(blank=True, max_length=5, null=True)),
                ('recentMedicine', models.CharField(blank=True, max_length=20, null=True)),
                ('recentMedicineTime', models.CharField(blank=True, max_length=20, null=True)),
                ('isDrugFast', models.CharField(blank=True, max_length=20, null=True)),
                ('drugFastTime', models.CharField(blank=True, max_length=20, null=True)),
                ('otherMedicine', models.CharField(blank=True, max_length=20, null=True)),
                ('medicineAndTime', models.CharField(blank=True, max_length=30, null=True)),
                ('IMM_Therapy', models.CharField(blank=True, max_length=10, null=True)),
                ('medicineName', models.CharField(blank=True, max_length=20, null=True)),
                ('medicineUseMonth', models.CharField(blank=True, max_length=20, null=True)),
                ('preoperative', models.CharField(blank=True, max_length=20, null=True)),
                ('isInGroup', models.CharField(blank=True, max_length=5, null=True)),
                ('inspectTimes', models.IntegerField(blank=True, null=True)),
                ('PD', models.CharField(blank=True, max_length=10, null=True)),
                ('smoking', models.CharField(blank=True, max_length=5, null=True)),
                ('packagePerDay', models.CharField(blank=True, max_length=10, null=True)),
                ('smokingYears', models.CharField(blank=True, max_length=10, null=True)),
                ('otherDisease', models.CharField(blank=True, max_length=10, null=True)),
                ('diseaseDescribe', models.CharField(blank=True, max_length=10, null=True)),
                ('therapyEffect', models.CharField(blank=True, max_length=10, null=True)),
                ('CEA', models.CharField(blank=True, max_length=10, null=True)),
                ('SCC', models.CharField(blank=True, max_length=10, null=True)),
                ('ProGRP', models.CharField(blank=True, max_length=10, null=True)),
                ('NSE', models.CharField(blank=True, max_length=10, null=True)),
                ('CA125', models.CharField(blank=True, max_length=10, null=True)),
                ('CA199', models.CharField(blank=True, max_length=10, null=True)),
                ('detectTime', models.DateField()),
                ('perTumorHistory', models.CharField(blank=True, max_length=10, null=True)),
                ('tumorName', models.CharField(blank=True, max_length=20, null=True)),
                ('confirmedAge', models.CharField(blank=True, max_length=2, null=True)),
                ('isRelativeTumor', models.CharField(blank=True, max_length=5, null=True)),
                ('tumorType', models.CharField(blank=True, max_length=10, null=True)),
                ('kinship', models.CharField(blank=True, max_length=10, null=True)),
                ('relativeAge', models.CharField(blank=True, max_length=10, null=True)),
                ('menarcheAge', models.CharField(blank=True, max_length=10, null=True)),
                ('menstrualCycle', models.CharField(blank=True, max_length=10, null=True)),
                ('firstPregnancyAge', models.CharField(blank=True, max_length=10, null=True)),
                ('pregnancyTimes', models.IntegerField(blank=True, null=True)),
                ('birthTimes', models.IntegerField(blank=True, null=True)),
                ('personalLactation', models.CharField(blank=True, max_length=20, null=True)),
                ('feedingTimes', models.CharField(blank=True, max_length=20, null=True)),
                ('menopauseStage', models.CharField(blank=True, max_length=10, null=True)),
                ('menopauseAge', models.CharField(blank=True, max_length=5, null=True)),
                ('isCheckBreast', models.CharField(blank=True, max_length=5, null=True)),
                ('smokeWineMedicine', models.CharField(blank=True, max_length=10, null=True)),
                ('contactHistory', models.CharField(blank=True, max_length=10, null=True)),
                ('breastSelfCheck', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CancerResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('batchId', models.CharField(blank=True, max_length=20, null=True)),
                ('classify', models.CharField(blank=True, max_length=20, null=True)),
                ('nutationType', models.CharField(blank=True, max_length=20, null=True)),
                ('gene', models.CharField(blank=True, max_length=20, null=True)),
                ('HGVS', models.CharField(blank=True, max_length=50, null=True)),
                ('rate', models.CharField(blank=True, max_length=20, null=True)),
                ('annoLd', models.CharField(blank=True, max_length=50, null=True)),
                ('annoLdRemark', models.CharField(blank=True, max_length=50, null=True)),
                ('isFirstLevel', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('receipt_date', models.DateField()),
                ('detect_content', models.CharField(blank=True, max_length=20, null=True)),
                ('inspect_date', models.DateField()),
                ('deadline', models.DateField()),
                ('report_date', models.DateField()),
                ('send_date', models.DateField()),
                ('is_scientific', models.CharField(choices=[('YES', '是'), ('NO', '否')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('serial_number', models.CharField(blank=True, max_length=20, null=True)),
                ('sale_price', models.CharField(blank=True, max_length=10, null=True)),
                ('is_charge', models.CharField(choices=[('YES', '是'), ('NO', '否')], max_length=5)),
                ('invoice_id', models.CharField(blank=True, max_length=30, null=True)),
                ('invoice_company', models.CharField(blank=True, max_length=30, null=True)),
                ('invoice_date', models.DateField()),
                ('invoice_amount', models.CharField(blank=True, max_length=10, null=True)),
                ('receipt_id', models.CharField(blank=True, max_length=30, null=True)),
                ('bank_charges', models.CharField(blank=True, max_length=10, null=True)),
                ('trade_receivable', models.CharField(blank=True, max_length=10, null=True)),
                ('actual_payment', models.CharField(blank=True, max_length=10, null=True)),
                ('settlement_price', models.CharField(blank=True, max_length=10, null=True)),
                ('cash_date', models.DateField()),
                ('cash_month', models.CharField(blank=True, max_length=10, null=True)),
                ('SP', models.CharField(blank=True, max_length=10, null=True)),
                ('voucher_id', models.CharField(default='输入用友凭证号', max_length=20)),
                ('promotion_expenses', models.CharField(blank=True, max_length=10, null=True)),
                ('promotion_date', models.DateField()),
                ('u8_month', models.DateField()),
                ('is_receipt', models.CharField(choices=[('YES', '是'), ('NO', '否')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ItemsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('project_type', models.CharField(default='实体瘤/血液病', max_length=10)),
                ('detect_content', models.CharField(default='检测内容', max_length=10)),
                ('detect_items', models.CharField(default='所属检测套餐', max_length=10)),
                ('detect_counts', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('sample_nation', models.CharField(blank=True, max_length=20, null=True)),
                ('sample_age', models.CharField(blank=True, max_length=20, null=True)),
                ('certificate_type', models.CharField(blank=True, max_length=10, null=True)),
                ('certificate_id', models.CharField(blank=True, max_length=18, null=True)),
                ('sample_name', models.CharField(blank=True, max_length=25, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=18, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_address', models.CharField(blank=True, max_length=100, null=True)),
                ('submit_physician', models.CharField(blank=True, max_length=20, null=True)),
                ('physician_phone', models.CharField(blank=True, max_length=18, null=True)),
                ('medical_record_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SaleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(default='HB00001', max_length=20)),
                ('cities', models.CharField(default='输入城市', max_length=10)),
                ('areas', models.CharField(default='输入地区', max_length=10)),
                ('market_represent', models.CharField(default='输入销售代表', max_length=10)),
                ('submit_hospital', models.CharField(default='输入送检医院', max_length=20)),
                ('departments', models.CharField(default='输入科室', max_length=10)),
                ('station', models.CharField(default='输入岗位', max_length=10)),
                ('in_charge', models.CharField(default='输入负责人', max_length=10)),
                ('DSM', models.CharField(default='输入直属领导', max_length=10)),
                ('sale_price', models.CharField(blank=True, max_length=10, null=True)),
                ('agency_direct', models.CharField(default='直营', max_length=5)),
            ],
        ),
    ]
