# _*_ coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

# Create your models here.

from company.models import Staff


class Project(models.Model):
    project_id = models.CharField(max_length=100, verbose_name='项目编号')
    start_date = models.DateField(auto_now=True, verbose_name='开始日期')
    end_date = models.DateField(blank=True, verbose_name='结束日期')
    head = models.ForeignKey(Staff, verbose_name='负责人')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
