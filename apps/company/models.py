# _*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Department(models.Model):
    """
    Description: 部门，用来定义公司的组织架构，目前只支持一层架构
    """
    department_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='部门名称')
    depart_level = models.IntegerField(default=0, verbose_name='部门级别')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.department_name


class Duty(models.Model):
    """
    Description: 部门下面的职位
    """
    department = models.ForeignKey(Department, verbose_name='部门')
    duty_name = models.CharField(max_length=20, verbose_name='职位名称')

    class Meta:
        verbose_name = '职位名称'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.duty_name


class Staff(AbstractUser):
    """
    Description: 公司成员信息
    """
    sex_char = (
        ('M', '男'),
        ('F', '女')
    )

    duty = models.ForeignKey(Duty, verbose_name='职位')
    staff_name = models.CharField(max_length=20, null=False, blank=False, verbose_name='姓名')
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(choices=sex_char, max_length=1, null=False, blank=False, verbose_name='性别')
    phone = models.CharField(null=True, blank=True, max_length=11, verbose_name='手机号码')

    class Meta:
        verbose_name = '公司成员'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.staff_name
