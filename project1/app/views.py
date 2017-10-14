"""
Definition of views.
"""
from xml.dom import minidom

from django.core.serializers import json
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from urllib.parse import urlparse

def home(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    import xml.etree.ElementTree as ET
    tree = ET.parse('news_ua.xml')
    root = tree.getroot()
    news = {}
    guid = []
    ids = []

    for child in root:
        title = child.find("title").text
        desc = child.find("description").text
        for child1 in child.findall('item'):
            guid += [child1.find('guid').text]
            news[child1.find('title').text] = [child1.find('description').text]

    for id in guid:
        o = urlparse(id)
        ids += [o.query]

    keys = news.keys()

    return render(
        request,
        'app/index.html',
        {
            'title': title,
            'description': desc,
            'guid':zip(keys,ids),

        }
    )



def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def createNew(request):
    assert isinstance(request, HttpRequest)
    import xml.etree.ElementTree as ET
    tree = ET.parse('news_ua.xml')
    root = tree.getroot()

    """'INDENT()' to ident new data in file. source: stack overflow"""
    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    if 'title' in request.POST and 'description' in request.POST:
        title = request.POST['title']
        description = request.POST['description']
        if title and description:
            channel = root.find('channel')
            item = ET.SubElement(channel, 'item')
            guid = ET.SubElement(item, 'guid')
            titulo = ET.SubElement(item, 'title')
            link = ET.SubElement(item, 'link')
            desc = ET.SubElement(item, 'description')
            pubDate = ET.SubElement(item, 'pubDate')
            titulo.text = title
            desc.text = description

            tree.write('news_ua.xml', encoding="utf-8", xml_declaration=True)


    return render(
        request,
        'app/createNew.html',
        {
            """"'guid': request.GET['id'],"""
            'year': datetime.now().year,
        }
    )



def about(request):
    assert isinstance(request, HttpRequest)
    import xml.etree.ElementTree as ET
    tree = ET.parse('news_ua.xml')
    root = tree.getroot()
    news = {}
    guid = []
    ids = []

    for child in root:
        title = child.find("title").text
        desc = child.find("description").text
        for child1 in child.findall('item'):
            guid += [child1.find('guid').text]
            news[child1.find('title').text] = [child1.find('description').text]

    for id in guid:
        o = urlparse(id)
        id = o.query.replace("c=", '')
        ids += [id]

    values = news.values()
    keys = news.keys()


    return render(
        request,
        'app/about.html',
        {
            'id': request.GET['c'],
            'news': zip(keys,ids, values),
            'year': datetime.now().year,
        }
    )

