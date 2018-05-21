"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import gemeinsammabrechnen


urlpatterns = [
    url(r'^', include('dashboard.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^uebersicht/', include('uebersicht.urls')),
    url(r'^addeinzelbuchung/', include('addeinzelbuchung.urls')),
    url(r'^addgemeinsam/', include('addgemeinsam.urls')),
    url(r'^production/', include('production.urls')),
    url(r'^gemeinsameuebersicht/', include('gemeinsamuebersicht.urls')),
    url(r'^monatsuebersicht/', include('monatsuebersicht.urls')),
    url(r'^gemeinsamabrechnen/', include('gemeinsammabrechnen.urls')),
    url(r'^abrechnen/$', gemeinsammabrechnen.views.abrechnen, name='abrechnen'),
    url(r'^import/', include('importd.urls')),
    url(r'^adddauerauftrag/', include('adddauerauftrag.urls')),
    url(r'^dauerauftraguebersicht/', include('dauerauftraguebersicht.urls')),
    url(r'^configuration/', include('configuration.urls')),
    url(r'^jahresuebersicht/', include('jahresuebersicht.urls')),
    url(r'^addeinnahme/', include('addeinnahme.urls')),
    url(r'^theme/', include('theme.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
