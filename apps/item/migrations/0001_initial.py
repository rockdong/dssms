# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-09 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u540d\u79f0')),
                ('num', models.IntegerField(default=0, verbose_name='\u6570\u91cf')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='\u7c7b\u522b')),
                ('parent', models.IntegerField(default=0, verbose_name='\u7236\u7c7bID')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.Type', verbose_name='\u7c7b\u522b'),
        ),
    ]
