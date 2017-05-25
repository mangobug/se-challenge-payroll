from django.conf.urls import url

from . import views

app_name = 'payroll'
urlpatterns = [
    url(r'^traverse/$', views.traverse, name='traverse'),
]
