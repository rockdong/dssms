# _*_ coding:utf-8 _*_

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.hashers import make_password
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from company.models import Staff, Department, Duty
from .forms import RegisterStaffForm

from utils.mixin_utils import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index.html', {})


class StaffView(LoginRequiredMixin, View):
    def get(self, request, value="所有"):
        departments = Department.objects.all()
        if value == "所有":
            staffs = Staff.objects.all()
        else:
            staffs = Staff.objects.filter(duty__department__department_name=value)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(staffs, 5, request=request)
        staffs = p.page(page)
        return render(request, 'staffs.html', {'staffs': staffs, 'deptname': value, 'departments': departments})

    def delete(self, request, value):
        if value != "":
            try:
                Staff.objects.get(username=value).delete()
                return HttpResponseRedirect('index/staffs/所有/')
            except Exception as e:
                return HttpResponse(json.dumps({"status": "fail", "msg": "删除失败"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "fail", "msg": "请选择删除的用户"}), content_type="application/json")

    # 添加用户
    def post(self, request, value):
        # 如果成功，刷新页面，如果失败，弹出对话框
        try:
            register_staff_form = RegisterStaffForm(request.POST)
            if register_staff_form.is_valid():
                username = request.POST.get('username', None)
                password = request.POST.get('password', None)
                sex = request.POST.get('sex', None)
                phone = request.POST.get('phone', None)
                staff_name = request.POST.get('staff_name', None)

                department = Department()
                department.department_name = "领导"
                department.save()

                duty = Duty()
                duty.department = department
                duty.duty_name = "董事"
                duty.save()

                staff = Staff()
                staff.duty = duty
                staff.staff_name = staff_name
                staff.sex = sex
                staff.phone = phone
                staff.username = username
                staff.password = make_password(password)
                staff.is_active = True
                staff.is_staff = True
                staff.save()

                return render(request, '', {})
            else:
                return render(request, '', {})
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "添加用户失败"}), content_type="application/json")


class DepartDutyView(LoginRequiredMixin, View):
    def get(self, request, value="所有"):
        try:
            depts = Department.objects.all()
            if value == "所有":
                dept = depts[0]
            else:
                dept = depts.get(department_name=value)
            dutys = Duty.objects.filter(department__department_name=dept.department_name)
            return render(request, 'add_duty.html', {'depts': depts, 'dept': dept.department_name, 'dutys': dutys})
        except Exception as e:
            return render(request, 'add_duty.html', {})

    def post(self, request, value):
        departname = request.POST.get('departmentname', None)

        dutyname = request.POST.get('dutyname', None)

        try:
            depart = Department.objects.get(department_name=departname)
        except Exception as e:
            depart = None

        if dutyname == "":
            if depart is None:
                dept = Department()
                dept.department_name = departname
                dept.save()
                return HttpResponse(json.dumps({"status": "success", "msg": "添加成功"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "添加失败, 该部门名称已存在"}), content_type="application/json")
        else:
            try:
                dutys = Duty.objects.get(department__department_name=depart.department_name, duty_name=dutyname)
            except Exception as e:
                dutys = None

            if dutys is None:
                duty = Duty()
                duty.department = depart
                duty.duty_name = dutyname
                duty.save()
                return HttpResponse(json.dumps({"status": "success", "msg": "添加成功"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "添加失败, 该部门名称已存在"}), content_type="application/json")

    def delete(self, request, value):
        # 使用 AJAX 调用, 从 request 中获取 数据
        departname = request.POST.get('departname', None)
        dutyname = request.POST.get('dutyname', None)
        try:
            if dutyname is not None:
                Duty.objects.get(duty_name=dutyname, department__department_name=departname).delete()
            else:
                Duty.objects.filter(department__department_name=departname).delete()
                Department.objects.get(department_name=departname).delete()
            return HttpResponse(json.dumps({"status": "success", "msg": "删除成功"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "删除失败"}), content_type="application/json")


class DepartsDutysView(View):
    def get(self, request):
        all_departs = Department.objects.all()
        all_dutys = Duty.objects.all()

        depart_duty = []
        for depart in all_departs:
            depart_duty.append(depart)

        for duty in all_dutys:
            depart_duty.append(duty)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(depart_duty, 5, request=request)
        dutys = p.page(page)
        return render(request, 'depts_dutys.html', {"dutys": dutys})

    def post(self, request):
        return HttpResponse(json.dumps({"status": "success", "msg": "删除成功"}), content_type="application/json")
