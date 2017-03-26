from django import forms
from company.models import Staff


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['username', 'password', 'staff_name', 'sex', 'phone']