from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views
import app.forms
import app.views

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
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
    url(r'^spotify_login/', app.views.spotify_login, name='spotify_login'),
    url(r'^spotify_logout/', app.views.spotify_logout, name='spotify_logout'),
    url(r'^register$', app.views.register, name='register'),
    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
