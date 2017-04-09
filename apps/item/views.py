# _*_ coding:utf-8 _*_

from django.shortcuts import render, HttpResponseRedirect

from django.views.generic import View

# Create your views here.


class AddTypeView(View):
    def get(self, request):
        return render(request, 'add_item_type.html', {})

    def post(self, request):
        return HttpResponseRedirect("type_add")
