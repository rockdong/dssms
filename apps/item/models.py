# _*_coding:utf-8_*_

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=10, verbose_name='类别')
    parent = models.IntegerField(default=0, verbose_name='父类ID')


class Item(models.Model):
    type = models.ForeignKey(Type, verbose_name='类别')
    name = models.CharField(max_length=20, verbose_name='名称')
    num = models.IntegerField(default=0, verbose_name='数量')