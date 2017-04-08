# _*_coding:utf-8 _*_

import json
import datetime

from django.shortcuts import render, HttpResponse
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from company.models import Staff

from .models import Project

from .forms import ProjectForm

# Create your views here.


class ProjectView(View):
    def get(self, request):
        all_project = Project.objects.all()
        if all_project:
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(all_project, 5, request=request)
            projects = p.page(page)
            return render(request, 'projects.html', {'projects': projects})
        else:
            return render(request, 'projects.html', {})


class ProjectAddView(View):
    def get(self, request):
        staffs = Staff.objects.all()
        return render(request, 'add_project.html', {"staffs": staffs})

    def post(self, request):
        try:
            project_form = ProjectForm(request.POST)
            if project_form.is_valid():
                project = Project()
                head = request.POST.get('head', '')
                project.head = Staff.objects.get(staff_name=head)
                project.project_id = request.POST.get('project_id', '')
                project.start_date = datetime.datetime.strptime(request.POST.get('start_date', ''), '%Y-%m-%d')
                project.end_date = datetime.datetime.strptime(request.POST.get('end_date', ''), '%Y-%m-%d')
                project.save()
                return HttpResponse(json.dumps({"status": "success", "msg": "工程删除成功!"}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "填写数据有误!"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "工程删除失败!"}), content_type="application/json")


class ProjectDeleteView(View):
    def post(self, request):
        try:
            id = request.POST.get('id', '')
            Project.objects.get(id=id).delete()
            return HttpResponse(json.dumps({"status": "success", "msg": "工程删除成功!"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "工程删除失败!"}), content_type="application/json")
