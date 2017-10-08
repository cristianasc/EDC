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
    tree = ET.parse('airport.xml')
    root = tree.getroot()
    code = {}
    source = {}
    planfeatures = []
    units = []
    coord = []
    cg = []

    """existing root tags"""
    for child in root:
        print(child.tag)

    """info about Project tag"""
    for child in root.findall('Project'):
        for child1 in child.iter('Feature'):
            code[child1.get('code')] = []
            source[child1.get('source')] = []
            for child2 in child1.iter('Property'):
                code[child1.get('code')].append(child2.get('label'))
                code[child1.get('code')].append(child2.get('value'))
                source[child1.get('source')].append(child1.get('code'))

    c = [code for code in code.keys()]
    s = [source for source in source.keys()]





    """info about PlanFeatures tag"""
    for child in root.findall('PlanFeatures'):
        for child1 in child.findall('PlanFeature'):
            for child2 in child1.iter('Feature'):
                for child3 in child2.iter('Property'):
                    planfeatures.append([child2.get('code'), child2.get('source'),child3.get('label'),child3.get('value')])

    """info about Units tag"""
    for child in root.findall('Units'):
        for child1 in child.findall('Imperial'):
                    units.append([child1.get('linearUnit'), child1.get('angularUnit'),
                                  child1.get('elevationUnit'), child1.get('latLongAngularUnit'),
                                  child1.get('areaUnit'),child1.get('temperatureUnit'),
                                  child1.get('pressureUnit'),child1.get('volumeUnit')])

    """info about CoordinateSystem tag"""
    for child in root.findall('CoordinateSystem'):
        for child1 in child.iter('Feature'):
            for child2 in child1.iter('Property'):
                coord.append([child1.get('code'), child1.get('source'),child2.get('label'),child2.get('value')])

    """info about CgPoints tag"""
    for child in root.findall('CgPoints'):
        for child1 in child.iter('CgPoint'):
                cg.append([child.get('name'), child1.get('name')])


    return render(
        request,
        'app/index.html',
        {
            'title':'Airport',
            'codes': zip(s,c),
            'year': datetime.now().year,

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

def about(request):
    assert isinstance(request, HttpRequest)
    import xml.etree.ElementTree as ET
    tree = ET.parse('airport.xml')
    root = tree.getroot()
    code = {}
    source = {}

    """info about Project tag"""
    for child in root.findall('Project'):
        for child1 in child.iter('Feature'):
            code[child1.get('code')] = []
            source[child1.get('source')] = []
            for child2 in child1.iter('Property'):
                code[child1.get('code')].append(child2.get('label'))
                code[child1.get('code')].append(child2.get('value'))
                source[child1.get('source')].append(child1.get('code'))

    c = [code for code in code.keys()]
    s = [source for source in source.keys()]


    return render(
        request,
        'app/about.html',
        {
            'codes': zip(c,s),
            'values': source,
            'guid': request.GET['id'],
        }
    )

