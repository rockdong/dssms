# _*_ coding:utf-8 _*_

from django.shortcuts import render
from django.core.serializers import serialize

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
from django.contrib.auth.hashers import make_password
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from company.models import Staff, Department, Duty
from company.forms import RegisterForm

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

    def post(self, request, value):
        try:
            id = request.POST.get('id', '')
            if id is not None:
                Staff.objects.get(id=id).delete()
                return HttpResponse(json.dumps({"status": "success", "msg": "删除成功!"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "输入错误"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "删除失败"}), content_type="application/json")


class StaffDetailView(LoginRequiredMixin, View):
    def get(self, request, value):
        try:
            staff = Staff.objects.get(id=value)
            depts = Department.objects.all()
            dutys = Duty.objects.filter(department__department_name=staff.duty.department.department_name)
            return render(request, 'staff_detail.html', {"staff": staff, })
        except Exception as e:
            return render(request, 'staff_detail.html', {})


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
        depart_level = request.POST.get('depart_level', None)

        dutyname = request.POST.get('dutyname', None)

        try:
            depart = Department.objects.get(department_name=departname)
        except Exception as e:
            depart = None

        if dutyname == "":
            if depart is None:
                dept = Department()
                dept.department_name = departname
                dept.depart_level = depart_level
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


class DepartsView(LoginRequiredMixin, View):
    def get(self, request):
        all_departs = Department.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_departs, 5, request=request)
        departs = p.page(page)
        return render(request, 'depts_dutys.html', {"departs": departs})

    def post(self, request):
        method = request.POST.get('method', None)
        if method == "delete":
            try:
                depart_name = request.POST.get('depart_name', '')
                if depart_name is not None:
                    Duty.objects.filter(department__department_name=depart_name).delete()
                    Department.objects.get(department_name=depart_name).delete()
                    return HttpResponse(json.dumps({"status": "success", "msg": "删除成功"}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({"status": "fail", "msg": "删除失败"}), content_type="application/json")
        elif method == "modify":
            try:
                org_depart_name = request.POST.get('org_depart_name', '')
                depart_name = request.POST.get('depart_name', '')
                if org_depart_name is not None:
                    depart = Department.objects.get(department_name=org_depart_name)
                    depart.department_name = depart_name
                    depart.save()
                    return HttpResponse(json.dumps({"status": "success", "msg": "删除成功"}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({"status": "fail", "msg": "删除失败"}), content_type="application/json")


class DepartDetailView(LoginRequiredMixin, View):
    def get(self, request, value):
        try:
            all_dutys = Duty.objects.filter(department__department_name=value)
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(all_dutys, 5, request=request)
            dutys = p.page(page)
            return render(request, 'dept_detail.html', {"dutys": dutys, "depart": value})
        except Exception as e:
            return render(request, 'dept_detail.html', {"depart": value})

    def post(self, request, value):
        try:
            method = request.POST.get('method', '')
            if method == "delete":
                try:
                    duty_name = request.POST.get('duty_name', '')
                    duty = Duty.objects.get(duty_name=duty_name)
                    duty.delete()
                    return HttpResponse(json.dumps({"status": "success", "msg": "删除成功!"}),
                                        content_type="application/json")
                except Exception as e:
                    return HttpResponse(json.dumps({"status": "fail", "msg": "删除失败!"}), content_type="application/json")
            elif method == "modify":
                try:
                    org_duty_name = request.POST.get('org_duty_name', '')
                    duty_name = request.POST.get('duty_name', None)
                    if duty_name is not None:
                        duty = Duty.objects.get(duty_name=org_duty_name)
                        duty.duty_name = duty_name
                        duty.save()
                        return HttpResponse(json.dumps({"status": "success", "msg": "修改成功!"}),
                                            content_type="application/json")
                    else:
                        return HttpResponse(json.dumps({"status": "fail", "msg": "修改失败!"}),
                                            content_type="application/json")
                except Exception as e:
                    return HttpResponse(json.dumps({"status": "fail", "msg": "修改失败!"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "错误操作!"}), content_type="application/json")


class AddStaffView(LoginRequiredMixin, View):
    def get(self, request, value):
        try:
            if value == "所有":
                all_departs = Department.objects.all()
                dutys = Duty.objects.filter(department__department_name=all_departs[0].department_name)
                return render(request, 'add_staffs.html', {"departs": all_departs, "dutys": dutys})
            else:
                departname = request.GET.get('departname', None)
                dutys = serialize("json", Duty.objects.filter(department__department_name=departname))
                return HttpResponse(json.dumps({"status":"success", "dutys":dutys}), content_type="application/json")
        except Exception as e:
            return render(request, 'add_staffs.html', {})

    # 添加用户
    def post(self, request, value):
        # 如果成功，刷新页面，如果失败，弹出对话框
        try:
            register_staff_form = RegisterForm(request.POST)
            if register_staff_form.is_valid():
                username = request.POST.get('username', None)
                password = request.POST.get('password', None)
                sex = request.POST.get('sex', None)
                phone = request.POST.get('phone', None)
                staff_name = request.POST.get('staff_name', None)
                departname = request.POST.get('department', None)
                dutyname = request.POST.get('duty_name', None)
                birthday = request.POST.get('birthday', None)

                duty = Duty.objects.get(duty_name=dutyname, department__department_name=departname)

                staff = Staff()
                staff.duty = duty
                staff.staff_name = staff_name
                staff.sex = sex
                staff.phone = phone
                staff.birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
                staff.username = username
                staff.password = make_password(password)
                staff.is_active = True
                staff.is_staff = True
                staff.is_superuser = False

                staff.save()

                return HttpResponse(json.dumps({"status": "success", "msg": "添加用户成功"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "添加用户失败"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "添加用户失败"}), content_type="application/json")