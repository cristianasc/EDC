"""webproj URL Configuration

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
from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views
from django.contrib.auth import views as auth_views


import app.forms
import app.views

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^register$', app.views.register, name='register'),
    url(r'^admin/', admin.site.urls),
    url(r'^get_all/', app.views.get_all, name='get_all'),
    url(r'^del_new/', app.views.del_new, name='del_new'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^see_more/', app.views.see_more, name='see_more'),
    url(r'^create_new/', app.views.create_new, name='create_new'),
]
