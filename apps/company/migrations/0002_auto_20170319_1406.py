# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-19 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
