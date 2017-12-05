# coding=utf-8
from acorndxData.configure import *
from django.db import models

# Create your models here.


class PersonInfo(models.Model):
    # 个人信息表
    sample_id = models.CharField(max_length=20, default='HB00001')
    sample_nation = models.CharField(max_length=20, null=True, blank=True)
    sample_age = models.CharField(max_length=20, null=True, blank=True)
    certificate_type = models.CharField(max_length=10, null=True, blank=True)
    certificate_id = models.CharField(max_length=18, null=True, blank=True)
    sample_name = models.CharField(max_length=25, null=True, blank=True)
    contact_phone = models.CharField(max_length=18, null=True, blank=True)
    contact_email = models.CharField(max_length=20, null=True, blank=True)
    contact_address = models.CharField(max_length=100, null=True, blank=True)
    submit_physician = models.CharField(max_length=20, null=True, blank=True)
    physician_phone = models.CharField(max_length=18, null=True, blank=True)
    medical_record_id = models.IntegerField()

    def __str__(self):
        return self.sample_id


class ItemsInfo(models.Model):
    # 项目信息表
    # 根据个人信息表自动更新counts
    project_type = models.CharField(max_length=10, default='实体瘤/血液病')
    detect_content = models.CharField(max_length=10, default='检测内容')
    detect_items = models.CharField(max_length=10, default='所属检测套餐')
    detect_counts = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.detect_content


class DetectInfo(models.Model):
    # 检测信息
    sample = models.ForeignKey(PersonInfo, on_delete=models.CASCADE, related_name='+')
    receipt_date = models.DateField()
    detect_content = models.ForeignKey(ItemsInfo, on_delete=models.CASCADE)
    inspect_date = models.DateField()
    deadline = models.DateField()
    report_date = models.DateField()
    send_date = models.DateField()
    is_scientific = models.CharField(max_length=2, choices=YES_OR_NO, default='否')

    def __int__(self):
        return self.sample


class FinancialRecord(models.Model):
    # 财务信息
    sample = models.ForeignKey(PersonInfo,
                               on_delete=models.CASCADE, related_name='+')
    serial_number = models.CharField(max_length=20, default='输入流水号')
    sale_price = models.FloatField(default=0)
    is_charge = models.CharField(max_length=5, choices=YES_OR_NO)
    invoice_id = models.CharField(max_length=30, blank=True, null=True)
    invoice_company = models.CharField(max_length=30, blank=True, null=True)
    invoice_date = models.DateField()
    invoice_amount = models.FloatField(default=0)
    receipt_id = models.CharField(max_length=30, blank=True, null=True)
    # receivable_way = models.CharField(max_length=10, default='输入回款方式')
    bank_charges = models.FloatField(blank=True, null=True)
    trade_receivable = models.FloatField(default=0)
    actual_payment = models.FloatField(default=0)
    settlement_price = models.FloatField(default=0)
    cash_date = models.DateField()
    cash_month = models.DateField()
    SP = models.CharField(max_length=10, null=True, blank=True)
    voucher_id = models.CharField(max_length=20, default='输入用友凭证号')
    promotion_expenses = models.FloatField(default=0)
    promotion_date = models.DateField()
    u8_month = models.DateField()
    is_receipt = models.CharField(max_length=5, choices=YES_OR_NO)


class SaleInfo(models.Model):
    # 销售信息
    sample = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    cities = models.CharField(max_length=10, default='输入城市')
    areas = models.CharField(max_length=10, default='输入地区')
    market_represent = models.CharField(max_length=10, default='输入销售代表')
    submit_hospital = models.CharField(max_length=20, default='输入送检医院')
    departments = models.CharField(max_length=10, default='输入科室')
    station = models.CharField(max_length=10, default='输入岗位')
    in_charge = models.CharField(max_length=10, default='输入负责人')
    DSM = models.CharField(max_length=10, default='输入直属领导')
    sale_price = models.FloatField(default=0)
    agency_direct = models.CharField(max_length=5, default='直营')


class BloodClinicInfo(models.Model):
    # 血液病临床信息表
    sample = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    takeTime = models.DateField(null=True, blank=True)
    detectTime = models.DateField(null=True, blank=True)
    importantFeature = models.CharField(max_length=30, null=True, blank=True)
    relevantHistory = models.CharField(max_length=30, null=True, blank=True)
    chemotherapy = models.CharField(max_length=20, null=True, blank=True)
    lastChemotherapy = models.DateField(null=True, blank=True)
    recentIMM = models.CharField(max_length=20, null=True, blank=True)
    specificIMM = models.CharField(max_length=20, null=True, blank=True)
    radiotherapy = models.CharField(max_length=20, null=True, blank=True)
    marrow = models.CharField(max_length=20, null=True, blank=True)
    WBC = models.CharField(max_length=20, null=True, blank=True)
    RBC = models.CharField(max_length=20, null=True, blank=True)
    Hb = models.CharField(max_length=20, null=True, blank=True)
    PLT = models.CharField(max_length=20, null=True, blank=True)
    primitiveCell = models.CharField(max_length=20, null=True, blank=True)
    juvenileCell = models.CharField(max_length=20, null=True, blank=True)
    otherCell = models.CharField(max_length=20, null=True, blank=True)
    marrowResult = models.CharField(max_length=30, null=True, blank=True)
    clinicalDiagnosis = models.CharField(max_length=30, null=True, blank=True)


class CancerClinicInfo(models.Model):
    # 实体瘤样本临床信息表
    sample = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    sampleType = models.CharField(max_length=10, null=True, blank=True)
    sendTogether = models.CharField(max_length=10, null=True, blank=True)
    tissueType = models.CharField(max_length=10, null=True, blank=True)
    primaryOrMet = models.CharField(max_length=10, null=True, blank=True)
    FFPE_date = models.DateField(null=True, blank=True)
    newTissue_date = models.DateField(null=True, blank=True)
    sampleSize = models.CharField(max_length=10, null=True, blank=True)
    getBloodTime = models.DateField(null=True, blank=True)
    timeState = models.CharField(max_length=10, null=True, blank=True)
    tissueTyping = models.CharField(max_length=10, null=True, blank=True)
    clinicalDiagnosis = models.CharField(max_length=20, null=True, blank=True)
    standardCD = models.CharField(max_length=20, null=True, blank=True)
    confirmedTime = models.DateField(null=True, blank=True)
    stateT = models.CharField(max_length=5, null=True, blank=True)
    stateN = models.CharField(max_length=5, null=True, blank=True)
    stateM = models.CharField(max_length=5, null=True, blank=True)
    clinicalStages = models.CharField(max_length=10, null=True, blank=True)
    recur = models.CharField(max_length=10, null=True, blank=True)
    transfer = models.CharField(max_length=10, null=True, blank=True)
    met = models.CharField(max_length=30, null=True, blank=True)
    ECOG = models.CharField(max_length=20, null=True, blank=True)
    operate_record = models.CharField(max_length=10, null=True, blank=True)
    operate_date = models.DateField(null=True, blank=True)
    radiotherapyRecord = models.CharField(max_length=5, null=True, blank=True)
    radioInitiation = models.CharField(max_length=30, null=True, blank=True)
    treatmentStage = models.CharField(max_length=10, null=True, blank=True)
    chemotherapy = models.CharField(max_length=10, null=True, blank=True)
    chemotherapyAndTime = models.CharField(max_length=100, null=True, blank=True)
    targetMedicine = models.CharField(max_length=5, null=True, blank=True)
    recentMedicine = models.CharField(max_length=20, null=True, blank=True)
    recentMedicineTime = models.CharField(max_length=20, null=True, blank=True)
    isDrugFast = models.CharField(max_length=20, null=True, blank=True)
    drugFastTime = models.CharField(max_length=20, null=True, blank=True)
    otherMedicine = models.CharField(max_length=20, null=True, blank=True)
    medicineAndTime = models.CharField(max_length=30, null=True, blank=True)
    IMM_Therapy = models.CharField(max_length=10, null=True, blank=True)
    medicineName = models.CharField(max_length=20, null=True, blank=True)
    medicineUseMonth = models.CharField(max_length=20, null=True, blank=True)
    preoperative = models.CharField(max_length=20, null=True, blank=True)
    isInGroup = models.CharField(max_length=5, null=True, blank=True)
    inspectTimes = models.IntegerField(null=True, blank=True)
    PD = models.CharField(max_length=10, null=True, blank=True)
    smoking = models.CharField(max_length=5, null=True, blank=True)
    packagePerDay = models.CharField(max_length=10, null=True, blank=True)
    smokingYears = models.CharField(max_length=10, null=True, blank=True)
    otherDisease = models.CharField(max_length=10, null=True, blank=True)
    diseaseDescribe = models.CharField(max_length=10, null=True, blank=True)
    therapyEffect = models.CharField(max_length=10, null=True, blank=True)
    CEA = models.CharField(max_length=10, null=True, blank=True)
    SCC = models.CharField(max_length=10, null=True, blank=True)
    ProGRP = models.CharField(max_length=10, null=True, blank=True)
    NSE = models.CharField(max_length=10, null=True, blank=True)
    CA125 = models.CharField(max_length=10, null=True, blank=True)
    CA199 = models.CharField(max_length=10, null=True, blank=True)
    detectTime = models.DateField(null=True, blank=True)
    perTumorHistory = models.CharField(max_length=10, null=True, blank=True)
    tumorName = models.CharField(max_length=20, null=True, blank=True)
    confirmedAge = models.CharField(max_length=2, null=True, blank=True)
    isRelativeTumor = models.CharField(max_length=5, null=True, blank=True)
    tumorType = models.CharField(max_length=10, null=True, blank=True)
    kinship = models.CharField(max_length=10, null=True, blank=True)
    relativeAge = models.CharField(max_length=10, null=True, blank=True)
    menarcheAge = models.CharField(max_length=10, null=True, blank=True)
    menstrualCycle = models.CharField(max_length=10, null=True, blank=True)
    firstPregnancyAge = models.CharField(max_length=10, null=True, blank=True)
    pregnancyTimes = models.IntegerField(null=True, blank=True)
    birthTimes = models.IntegerField(null=True, blank=True)
    personalLactation = models.CharField(max_length=20, null=True, blank=True)
    feedingTimes = models.CharField(max_length=20, null=True, blank=True)
    menopauseStage = models.CharField(max_length=10, null=True, blank=True)
    menopauseAge = models.CharField(max_length=5, null=True, blank=True)
    isCheckBreast = models.CharField(max_length=5, null=True, blank=True)
    smokeWineMedicine = models.CharField(max_length=10, null=True, blank=True)
    contactHistory = models.CharField(max_length=10, null=True, blank=True)
    breastSelfCheck = models.CharField(max_length=10, null=True, blank=True)


class CancerResult(models.Model):
    # 实体瘤检测结果
    sample = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    batchId = models.CharField(max_length=20, null=True, blank=True)
    classify = models.CharField(max_length=20, null=True, blank=True)
    nutationType = models.CharField(max_length=20, null=True, blank=True)
    gene = models.CharField(max_length=20, null=True, blank=True)
    HGVS = models.CharField(max_length=50, null=True, blank=True)
    rate = models.CharField(max_length=20, null=True, blank=True)
    annoLd = models.CharField(max_length=50, null=True, blank=True)
    annoLdRemark = models.CharField(max_length=50, null=True, blank=True)
    isFirstLevel = models.CharField(max_length=10, null=True, blank=True)


class BloodResult(models.Model):
    # 血液病检测结果
    sample = models.ForeignKey(PersonInfo, on_delete=models.CASCADE)
    confirmDisease = models.CharField(max_length=20, null=True, blank=True)
    confirmTime = models.CharField(max_length=20, null=True, blank=True)
    remark = models.CharField(max_length=20, null=True, blank=True)
    isPTD = models.CharField(max_length=10, null=True, blank=True)
    isNegative = models.CharField(max_length=10, null=True, blank=True)
    isMultiSite = models.CharField(max_length=10, null=True, blank=True)
    geneNumber = models.CharField(max_length=5, null=True, blank=True)
