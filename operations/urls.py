# _*_ coding:utf-8 _*_
__author__ = 'caidong'
__date__ = '2017/3/19 21:12'


from django.conf.urls import url

from operations.views import IndexView, StaffView, DepartDutyView, DepartsDutysView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^staffs/(?P<value>.*)/', StaffView.as_view(), name='staffs'),
    url(r'^depart_duty/(?P<value>.*)/', DepartDutyView.as_view(), name='depart_duty'),
    url(r'^departs_dutys/', DepartsDutysView.as_view(), name='departs_dutys'),
]
