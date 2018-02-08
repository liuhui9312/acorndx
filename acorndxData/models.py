# coding=utf-8
from django.db import models
# Create your models here.


class DataStructure(models.Model):
    itemsId = models.IntegerField()
    itemsChinese = models.CharField(max_length=10, default='中文列名')
    itemsEnglish = models.CharField(max_length=20, default='English')
    itemsType = models.CharField(max_length=5, default='char',
                                 choices=(('char', '字符'),
                                          ('int', '整数'),
                                          ('float', '浮点数'),
                                          ('date', '日期')))
    itemsLength = models.IntegerField(default=20)
    isNull = models.CharField(max_length=5, null=True, choices=(('True', '是'),
                                                                ('False', '否')))
    isBlank = models.CharField(max_length=5, null=True, choices=(('True', '是'),
                                                                 ('False', '否')))
    belongTable = models.CharField(max_length=20, null=False, blank=False)
    readRight = models.CharField(max_length=10, default='0')
    writeRight = models.CharField(max_length=10, default='0')
    illegality = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.itemsChinese

    class Meta:
        unique_together = (('belongTable', 'itemsEnglish'),)


class Department(models.Model):
    departmentId = models.IntegerField()
    departmentName = models.CharField(max_length=20, default='departmentName')
    department = models.CharField(max_length=20, default='department')

    def __str__(self):
        return self.departmentName


class UserInfo(models.Model):
    userName = models.CharField(max_length=10, default='username')
    userDepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
    account = models.CharField(max_length=20, null=True, blank=True)
    userRight = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.userName
