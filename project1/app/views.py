"""
Definition of views.
"""
from xml.dom import minidom

from BaseXClient import BaseXClient
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime, time
from time import gmtime, strftime
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, tostring
from .models import Database


def get_all(request):
    db = Database()
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
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    """
       tree = ET.parse('news_ua.xml')
       root = tree.getroot()
       news1 = {}
       for child in root:
           title = child.find("title").text
           description = child.find("description").text
           for child1 in child.findall('item'):
               guid += [child1.find('guid').text]
               news1[child1.find('title').text] = [child1.find('description').text]
    """

    ids = []
    title = ""

    db = Database()
    news, guid = db.news()

    keys = news.keys()

    for id in guid:
        o = urlparse(id)
        ids += [o.query]



    return render(
        request,
        'app/index.html',
        {
            'title': title,
            'guid': zip(keys, ids),

        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def createNew(request):
    assert isinstance(request, HttpRequest)
    tree = ET.parse('news_ua.xml')
    root = tree.getroot()
    ids = []
    guids = []

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

    for child in root:
        for child1 in child.findall('item'):
            guids += [child1.find('guid').text]

    for id in guids:
        o = urlparse(id)
        id = o.query.replace("c=", '')
        ids += [id]

    next_id = 6000+1

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
            guid.text = "https://uaonline.ua.pt/pub/detail.asp?c="+ str(next_id)
            link.text = "https://uaonline.ua.pt/pub/detail.asp?c=" + str(next_id)
            desc.text = description
            pubDate.text = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

            #tree.write('news_ua.xml', encoding="utf-8", xml_declaration=True)

            db = Database()
            db.add_new(tostring(item, encoding="unicode"))

    return render(
        request,
        'app/createNew.html',
        {
            'year': datetime.now().year,
        }
    )


def about(request):
    assert isinstance(request, HttpRequest)

    ids = []

    """
    tree = ET.parse('news_ua.xml')
    root = tree.getroot()
    news = {}
    guid = []
    for child in root:
        for child1 in child.findall('item'):
            guid += [child1.find('guid').text]
            news[child1.find('title').text] = [child1.find('description').text]
    """

    db = Database()
    news, guid = db.news()

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
            'news': zip(keys, ids, values),
            'year': datetime.now().year,
        }
    )