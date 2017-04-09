from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=10, verbose_name='类别')
    parent = models.IntegerField(default=0, verbose_name='父类ID')
    is_root = models.BooleanField(default=False, verbose_name='是根类别')


class Item(models.Model):
