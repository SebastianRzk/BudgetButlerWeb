from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^abrechnung/$', views.abrechnen),
    url(r'^$', views.index, name='index'),
]
