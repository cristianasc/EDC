"""
Definition of views.
"""
from django.core.serializers import json
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def home(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    import xml.etree.ElementTree as ET
    tree = ET.parse('news_ua.xml')
    root = tree.getroot()


    for child in root:
        print(child.tag)

    """info about Project tag"""
    for child in root:
        title = child.find("title").text
        desc = child.find("description").text


        """
        for child1 in child.iter('Feature'):
            code[child1.get('code')] = []
            source[child1.get('source')] = []
            for child2 in child1.iter('Property'):
                code[child1.get('code')].append(child2.get('label'))
                code[child1.get('code')].append(child2.get('value'))
                source[child1.get('source')].append(child1.get('code'))"""

    return render(
        request,
        'app/index.html',
        {
            'title': title,
            'description': desc,

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

    return render(
        request,
        'app/about.html',
        {
            """"'guid': request.GET['id'],"""
            'year': datetime.now().year,
        }
    )

