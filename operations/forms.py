# _*_coding:utf-8 _*_

from django import forms


class RegisterStaffForm(forms.Form):
    duty = forms.CharField(required=True)
    staff_name = forms.CharField(required=True, max_length=20)
    birthday = forms.DateField(required=True)
    sex = forms.CharField(required=True)
    phone = forms.CharField(required=True, min_length=11, max_length=11)