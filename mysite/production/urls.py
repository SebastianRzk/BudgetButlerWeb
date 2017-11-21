from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^testmode/$', views.enter_testmode),
    url(r'^$', views.leave_debug, name='index')
]
