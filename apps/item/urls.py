from django.conf.urls import url

from .views import AddTypeView

urlpatterns = [
    url(r'^type_add/', AddTypeView.as_view(), name='type_add'),
]
