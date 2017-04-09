# _*_ coding:utf-8 _*_
__author__ = 'caidong'
__date__ = '2017/4/5 17:04'


from django import forms


class ProjectForm(forms.Form):
    project_id = forms.CharField(required=True)
    head = forms.CharField(required=True)
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
