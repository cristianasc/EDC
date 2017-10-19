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


def upload_image(request):
    assert isinstance(request, HttpRequest)

    name = str(uuid.uuid4)
    default_storage.save(os.path.join(settings.BASE_DIR, 'images/'+name+'.png'), ContentFile(request.FILES['file'].read()))

    return render(
        request,
        'app/index.html',
        {

        }
    )


def create_new(request):
    assert isinstance(request, HttpRequest)

    title = request.POST.get("title")
    description = request.POST.get("description")

    root = ET.Element('item')
    guid_child = ET.SubElement(root, "guid")
    guid_child.text = "https://uaonline.ua.pt/pub/detail.asp?c=" + str(uuid.uuid4())

    title_child = ET.SubElement(root, "title")
    title_child.text = title

    link_child = ET.SubElement(root, "link")
    link_child.text = ""

    description_child = ET.SubElement(root, "description")
    description_child.text = description

    date_child = ET.SubElement(root, "pubDate")
    date_child.text = str(datetime.now())

    xmlstr = ET.tostring(root, encoding='utf8', method='xml')

    print(xmlstr.decode().replace("<?xml version='1.0' encoding='utf8'?>", ""))
    Database().add_new(xmlstr.decode().replace("<?xml version='1.0' encoding='utf8'?>", ""))

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