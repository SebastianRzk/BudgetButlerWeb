from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.leave_debug, name='index'),

]
