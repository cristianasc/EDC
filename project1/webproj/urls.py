from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views
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
    url(r'^comments/', app.views.comments, name='comments'),
    url(r'^del_new/', app.views.del_new, name='del_new'),
    url(r'^like_ranking/', app.views.like_ranking, name='like_ranking'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^create_new/', app.views.create_new, name='create_new'),
]
