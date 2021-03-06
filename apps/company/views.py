# _*_coding:utf-8 _*_

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.views.generic import View

import json
import datetime

from company.forms import LoginForm, RegisterForm

from utils.mixin_utils import LoginRequiredMixin

from company.models import Staff, Department, Duty

# Create your views here.


class LoginView(View):
    def get(self, request):
        if Staff.objects.filter(is_superuser=True):
            has_superuser = True
        else:
            has_superuser = False
        return render(request, "login.html", {'has_superuser':has_superuser})

    def post(self, request):
        login_form = LoginForm(request.POST)

        if not Staff.objects.filter(is_superuser=True):
            has_superuser = False
            return render(request, "login.html", {'has_superuser':has_superuser, 'error_msg':"请先注册管理员账号再登陆"})
        else:
            has_superuser = True

        if login_form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('index/')
            else:
                return render(request, 'login.html', {'error_msg':"登陆失败，用户名或密码错误", 'has_superuser':has_superuser})
        else:
            return render(request, 'login.html', {'login_form': login_form, 'has_superuser':has_superuser})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class RegisterView(View):
    def get(self, request):
        if Staff.objects.filter(is_superuser=True):
            # 如果有管理员账号，则返回登陆界面
            return render(request, "login.html", {'has_superuser': True})
        else:
            # 没有管理员账号才允许注册
            return render(request, 'regist.html', {})

    def post(self, request):
        # 如果成功，刷新页面，如果失败，弹出对话框
        try:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                username = request.POST.get('username', None)
                password = request.POST.get('password', None)
                sex = request.POST.get('sex', None)
                phone = request.POST.get('phone', None)
                staff_name = request.POST.get('staff_name', None)
                departname = request.POST.get('department', None)
                dutyname = request.POST.get('duty_name', None)
                birthday = request.POST.get('birthday', None)

                department = Department()
                department.department_name = departname
                department.save()

                duty = Duty()
                duty.department = department
                duty.duty_name = dutyname
                duty.save()

                staff = Staff()
                staff.duty = duty
                staff.staff_name = staff_name
                staff.sex = sex
                staff.phone = phone
                staff.username = username
                staff.birthday = datetime.datetime.strptime(birthday,'%Y-%m-%d')
                staff.password = make_password(password)
                staff.is_active = True
                staff.is_staff = True

                if Staff.objects.filter(is_superuser=True):
                    staff.is_superuser = False
                else:
                    staff.is_superuser = True

                staff.save()

                return HttpResponse(json.dumps({"status": "success", "msg": "添加用户成功"}), content_type="application/json")
            else:
                return render(request, 'regist.html', {"register_form": register_form})
        except Exception as e:
            return render(request, 'regist.html', {"register_form": register_form})