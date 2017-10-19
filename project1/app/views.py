"""
Definition of views.
"""

import os
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
from xml.dom import minidom
from django.http.response import HttpResponseBadRequest


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


def home(request):
    assert isinstance(request, HttpRequest)

    news = Database().news()
    Database().validate_xml()

    return render(
        request,
        'app/index.html',
        {
            'data': news
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
        description_child.text = '<img src="http://'+request.META['HTTP_HOST']+'/static/'+new_uuid+'.png" alt="'+title+'" title="'+title+'" style="width:70px;"/> ' + description

        date_child = ET.SubElement(root, "pubDate")
        date_child.text = str(datetime.now())

        xmlstr = ET.tostring(root, encoding='utf8', method='xml')

        print(xmlstr.decode().replace("<?xml version='1.0' encoding='utf8'?>", ""))
        Database().add_new(xmlstr.decode().replace("<?xml version='1.0' encoding='utf8'?>", ""))

        default_storage.save(os.path.join(settings.BASE_DIR, 'static/' + new_uuid + '.png'),
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
            return render(
                request,
                'app/index.html')
    else:
        form = RegistrationForm()
        x = {'form': form}
        return render(
                request,
                'app/register.html', x)


def about(request):
    assert isinstance(request, HttpRequest)

    if "c" not in request.GET:
        raise Exception("Erro: notícia não identificada.")

    selected_new = Database().get_new(request.GET["c"])

    return render(
        request,
        'app/about.html',
        {
            'data': selected_new
        }
    )