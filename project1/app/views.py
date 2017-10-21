import os
from BaseXClient import BaseXClient
from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime, time
from time import gmtime, strftime
from django.core.files.storage import default_storage
import xml.etree.ElementTree as ET
import uuid
from .models import Database
from django.core.files.base import ContentFile
from webproj import settings
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxml import html
import requests


@login_required
def like_ranking(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        social_user = request.user.social_auth.filter(
            provider='facebook',
        ).first()

        if "like" in request.POST:
            Database().like(social_user.uid, request.POST["like"], request.POST["guid"])
        else:
            Database().dislike(social_user.uid, request.POST["dislike"], request.POST["guid"])

    top_news_ids = Database().get_favorites(3)

    news = []

    for key, value in top_news_ids.items():
        news += [Database().get_new(value)]

    print(news)

    return render(
        request,
        'app/ranking.html',
        {
            'data': news
        }
    )


@login_required
def comments(request):
    assert isinstance(request, HttpRequest)

    try:
        social_user = request.user.social_auth.filter(
            provider='facebook',
        ).first()

        Database().comment(social_user.uid, social_user.user.first_name + " " + social_user.user.last_name, request.POST["comment"], request.POST["new_id"])


    except:
        pass

    return render(
        request,
        'app/about.html',
        {
            'hora': ""
        }
    )


def home(request):
    assert isinstance(request, HttpRequest)

    Database().validate_xml()

    Database().likes_xml()

    likes = {}

    for i in Database().news():
        likes[i["guid"]] = []
        likes[i["guid"]] += Database().get_likes(i["guid"])

    return render(
        request,
        'app/index.html',
        {
            'data': Database().news(),
            'likes': likes,
        }
    )


@login_required
def create_new(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":

        if "file" not in request.FILES:
            return HttpResponseBadRequest()

        title = request.POST.get("title")
        description = request.POST.get("description")
        abstract = request.POST.get("link")

        root = ET.Element('item')
        guid_child = ET.SubElement(root, "guid")
        new_uuid = str(uuid.uuid4())
        guid_child.text = new_uuid

        title_child = ET.SubElement(root, "title")
        title_child.text = title

        link_child = ET.SubElement(root, "link")
        link_child.text = abstract

        description_child = ET.SubElement(root, "description")
        description_child.text = '<img src="http://'+request.META['HTTP_HOST']+'/static/images/'+new_uuid+'.png" alt="'+title+'" title="'+title+'" style="width:70px;"/> ' + description

        date_child = ET.SubElement(root, "pubDate")
        date_child.text = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

        xmlstr = ET.tostring(root, encoding='utf8', method='xml')

        Database().add_new(xmlstr.decode().replace("<?xml version='1.0' encoding='utf8'?>", ""), new_uuid)

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


@login_required
def del_new(request):

    if request.method == 'POST':
        uid = request.POST.get("uid")
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

    try:
        social_user = request.user.social_auth.filter(
            provider='facebook',
        ).first()

        photo_url = "http://graph.facebook.com/%s/picture?type=large" % social_user.uid
        user_name = social_user.user.first_name + " " + social_user.user.last_name

    except AttributeError:
        photo_url = None
        user_name = None

    if "c" not in request.GET:
        return HttpResponseBadRequest("Erro: notícia não identificada.")

    selected_new = Database().get_new(request.GET["c"])
    comments = Database().get_comments(selected_new.get("guid"))

    if ("https://uaonline.ua.pt/pub/detail.asp?c=") in selected_new.get("link"):
        page = requests.get(selected_new.get("guid"))
        tree = html.fromstring(page.content)

        textbody = tree.xpath('//*[@id="contents"]/div[7]/p/text()')
    else:
        textbody = selected_new.get("link")

    return render(
        request,
        'app/about.html',
        {
            'data': selected_new,
            'textbody': textbody,
            'user_name': user_name,
            'new_id': selected_new.get("guid"),
            'photo': photo_url,
            'comments': comments
        }
    )
