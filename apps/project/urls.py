# _*_coding:utf-8_*_

from django.conf.urls import url

from project.views import ProjectView, ProjectAddView, ProjectDeleteView

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='project'),
    url(r'^project_add/', ProjectAddView.as_view(), name='project_add'),
    url(r'^project_delete/', ProjectDeleteView.as_view(), name='project_delete'),
]
