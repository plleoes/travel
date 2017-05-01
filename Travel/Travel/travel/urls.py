"""Travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
# from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import  url, include

from travel.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = {
    # Examples:
    # url(r'^$', 'Pablo1.views.home', name='home'),
    url(r'^$', my_view_index, name='index'),
    url(r'^registrationta.html$', my_view_registrationta, name='registration'),
    url(r'^registrationto.html$', my_view_registrationto, name='registration'),
    url(r'^regta.html$', my_view_regta, name='regta'),
    url(r'^regto.html$', my_view_regto, name='regto'),
    url(r'^webta$', my_view_webta, name='webta'),
    url(r'^webto$', my_view_webto, name='webto'),
    url(r'^forgetemail.html$', my_view_forgetemail, name='forgetemail'),
    url(r'^forget$', my_view_forget, name='forget'),
    url(r'^upd$', my_view_upd, name='upd'),
    url(r'^rspd$', my_view_rspd, name='rspd'),
    url(r'^regcancelpolicy$', my_view_regcancelpolicy, name='regcancelpolicy'),
    url(r'^regdefm$', my_view_regdefm, name='regdefm'),
    url(r'^up$', my_view_up, name='up'),
    url(r'^terms$', my_view_terms, name='terms'),
    url(r'^tsearch$', my_view_tsearch, name='tsearch'),
    url(r'^pack', my_view_pack, name='pack'),


}