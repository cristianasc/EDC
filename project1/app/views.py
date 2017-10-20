"""
Definition of views.
"""

import os
from urllib.request import urlopen

from BaseXClient import BaseXClient
from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.core.files.storage import default_storage
import xml.etree.ElementTree as ET
import uuid
from .models import Database
from django.core.files.base import ContentFile
from webproj import settings
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from requests import request, HTTPError


def get_all(request):
    Database()
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    input = "xquery doc('database')"
    query = session.execute(input)
    print(query)
    session.close()
    return render(
        request,
        'app/index.html',
        {
            'title': "OK"
        }
    )


@login_required
def home(request):
    assert isinstance(request, HttpRequest)

    Database().validate_xml()
    social_user = request.user.social_auth.filter(
        provider='facebook',
    ).first()
    photo_url = "http://graph.facebook.com/%s/picture?type=large" % social_user.uid

    print("ok")

    return render(
        request,
        'app/index.html',
        {
            'data': Database().news()
        }
    )


def create_new(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":

        if "file" not in request.FILES:
            return HttpResponseBadRequest()

        title = request.POST.get("title")
        description = request.POST.get("description")

        root = ET.Element('item')
        guid_child = ET.SubElement(root, "guid")
        new_uuid = str(uuid.uuid4())
        guid_child.text = new_uuid

        title_child = ET.SubElement(root, "title")
        title_child.text = title

        link_child = ET.SubElement(root, "link")
        link_child.text = ""

        description_child = ET.SubElement(root, "description")
        description_child.text = '<img src="http://'+request.META['HTTP_HOST']+'/static/images/'+new_uuid+'.png" alt="'+title+'" title="'+title+'" style="width:70px;"/> ' + description

        date_child = ET.SubElement(root, "pubDate")
        date_child.text = str(datetime.now())

        xmlstr = ET.tostring(root, encoding='utf8', method='xml')

        print(xmlstr.decode().replace("<?xml version='1.0' encoding='utf8'?>", ""))
        Database().add_new(xmlstr.decode().replace("<?xml version='1.0' encoding='utf8'?>", ""))

        default_storage.save(os.path.join(settings.BASE_DIR, 'static/images/' + new_uuid + '.png'),
                             ContentFile(request.FILES['file'].read()))

    return render(
        request,
        'app/createNew.html',
        {
            'year': datetime.now().year,
        }
    )


def register(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()
        return render(request, 'app/register.html', {'form': form})


def del_new(request):

    if request.method == 'POST':
        uid = request.POST.get("uid")
        print(uid)
        Database().del_new(uid)

        # delete new's img if exists
        path = os.path.join(settings.BASE_DIR, 'static/images/'+uid+'.png')
        if os.path.exists(path):
            os.system("rm " + path)

    return render(
        request,
        'app/delNew.html',
        {
            'data': Database().news()
        }
    )


def about(request):
    assert isinstance(request, HttpRequest)

    if "c" not in request.GET:
        return HttpResponseBadRequest("Erro: notícia não identificada.")

    selected_new = Database().get_new(request.GET["c"])

    return render(
        request,
        'app/about.html',
        {
            'data': selected_new
        }
    )


def update_likes(request):
    pass