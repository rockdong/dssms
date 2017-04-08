from django import forms
from company.models import Staff


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    staff_name = forms.CharField(required=True)
    sex = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    birthday = forms.DateField(required=True)
    department = forms.CharField(required=True)
    duty_name = forms.CharField(required=True)