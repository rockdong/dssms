# _*_ coding:utf-8 _*_
__author__ = 'caidong'
__date__ = '2017/3/19 21:12'


from django.conf.urls import url

from operations.views import IndexView, StaffView, DepartDutyView, DepartsView, AddStaffView, \
    DepartDetailView, StaffDetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^staffs/(?P<value>.*)/', StaffView.as_view(), name='staffs'),
    url(r'^staff_detail/(?P<value>.*)/', StaffDetailView.as_view(), name='staff_detail'),
    url(r'^depart_duty/(?P<value>.*)/', DepartDutyView.as_view(), name='depart_duty'),
    url(r'^departs/', DepartsView.as_view(), name='departs'),
    url(r'^dept_detail/(?P<value>.*)/', DepartDetailView.as_view(), name='dept_detail'),
    url(r'^add_staff/(?P<value>.*)/', AddStaffView.as_view(), name='add_staff'),
]
