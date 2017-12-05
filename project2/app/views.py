from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
import spotipy
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
from .models import Database
import requests
import json
from wikidata.client import Client
import ssl
import xmltodict


def home(request):
    db = Database()
    new_releases = db.get_new_releases()

    #try:
    """Verify if the user is logged in"""
    if request.COOKIES.get("SpotifyToken"):
        token = request.COOKIES.get("SpotifyToken")
        headers = {"Authorization": "Bearer " + token}
        r = requests.get('https://api.spotify.com/v1/me', headers=headers)
        r = json.loads(r.text)

        return render(
            request,
            'app/index.html',
            {
                'username': r["display_name"],
                'photo': r["images"][0]["url"],
                'artists': new_releases
            }
        )

    return render(
        request,
        'app/index.html',
        {
            'username': "",
            'artists': new_releases
        }
    )

    #except:
    #    return HttpResponseRedirect("/spotify_logout/")


def new_releases(request):
    scope = "user-library-read"
    client_credentials_manager = SpotifyOAuth(client_id='e31546dc73154ddaab16538209d8526e',
                                              client_secret='f12c6904e491409bbc5834aaa86d14c0', scope=scope,
                                              redirect_uri='http://localhost:8000')
    if "code" in request.GET:
        code = request.GET.get("code")
        token = client_credentials_manager.get_access_token(code)
        sp = spotipy.Spotify(auth=token["access_token"])
    else:
        authorize_url = client_credentials_manager.get_authorize_url()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return redirect(authorize_url)

    headers = {"Authorization": "Bearer " + token["access_token"]}
    r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=headers)
    xmlString = xmltodict.unparse(json.loads(r.text), pretty=True)
    file = open("new-releases.xml", "w")
    file.write(xmlString)

    return render(
        request,
        'app/index.html',
        {
            'data': ""
        }
    )


def top_tracks(request):
    scope = "user-top-read"
    client_credentials_manager = SpotifyOAuth(client_id='e31546dc73154ddaab16538209d8526e',
                                              client_secret='f12c6904e491409bbc5834aaa86d14c0', scope=scope,
                                              redirect_uri='http://localhost:8000')
    if "code" in request.GET:
        code = request.GET.get("code")
        token = client_credentials_manager.get_access_token(code)
        sp = spotipy.Spotify(auth=token["access_token"])
    else:
        authorize_url = client_credentials_manager.get_authorize_url()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return redirect(authorize_url)

    headers = {"Authorization": "Bearer " + token["access_token"]}
    r = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
    xmlString = xmltodict.unparse(json.loads(r.text), pretty=True)
    print(xmlString)
    file = open("top-tracks.xml", "w")
    file.write(xmlString)

    return render(
        request,
        'app/index.html',
        {
            'data': ""
        }
    )

def get_albuns_by_artist(request):
    assert isinstance(request, HttpRequest)

    def show_artist_albums(artist):
        albums = []
        results = sp.artist_albums(artist['id'], album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])
        seen = set()  # to avoid dups
        albums.sort(key=lambda album: album['name'].lower())
        for album in albums:
            name = album['name']
            if name not in seen:
                print((' ' + name))
                seen.add(name)

    def get_artist(name):
        results = sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            return items[0]
        else:
            return None

    scope = "user-library-read"
    client_credentials_manager = SpotifyOAuth(client_id='e31546dc73154ddaab16538209d8526e',
                                              client_secret='f12c6904e491409bbc5834aaa86d14c0', scope=scope,
                                              redirect_uri='http://localhost:8000')
    if "code" in request.GET:
        code = request.GET.get("code")
        token = client_credentials_manager.get_access_token(code)
        sp = spotipy.Spotify(auth=token["access_token"])

        artist = get_artist("Miley Cyrus")
        show_artist_albums(artist)

        return render(
            request,
            'app/index.html',
            {
                'data': ""
            }
        )
    else:
        authorize_url = client_credentials_manager.get_authorize_url()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return redirect(authorize_url)


def get_playlists_per_user(request):
    scope = "user-library-read"
    client_credentials_manager = SpotifyOAuth(client_id='e31546dc73154ddaab16538209d8526e',
                                              client_secret='f12c6904e491409bbc5834aaa86d14c0', scope=scope,
                                              redirect_uri='http://localhost:8000')
    if "code" in request.GET:
        code = request.GET.get("code")
        token = client_credentials_manager.get_access_token(code)

        sp = spotipy.Spotify(auth=token["access_token"])

        playlists = sp.user_playlists("danielapereirasimoes")
        for playlist in playlists['items']:
            print(playlist['name'])

        return render(
            request,
            'app/index.html',
            {
                'data': ""
            }
        )
    else:

        authorize_url = client_credentials_manager.get_authorize_url()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return redirect(authorize_url)


def login(request):
    return render(
        request,
        'app/index.html',
        {
            'data': ""
        }
    )

def artist(request):
    return render(
        request,
        'app/artistBio.html',
        {
            'data': ""
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
            # error
            return render(request, 'app/register.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'app/register.html', {'form': form})


def spotify_login(request):
    assert isinstance(request, HttpRequest)

    scope = ""
    client_credentials_manager = SpotifyOAuth(client_id='e31546dc73154ddaab16538209d8526e',
                                              client_secret='f12c6904e491409bbc5834aaa86d14c0', scope=scope,
                                              redirect_uri='http://localhost:8000/spotify_login/')
    spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    authorize_url = client_credentials_manager.get_authorize_url()

    if request.method == 'GET':
        if "code" in request.GET:
            code = request.GET.get("code")
            token = client_credentials_manager.get_access_token(code)
            token = token["access_token"]

            response = HttpResponseRedirect("/")
            response.set_cookie("SpotifyToken", token)

            return response
        else:
            return HttpResponseRedirect(authorize_url)


def spotify_logout(request):
    assert isinstance(request, HttpRequest)

    response = HttpResponseRedirect("/")
    response.delete_cookie("SpotifyToken")

    return response


def wikidata(request):

    """
        Override the SSL verification
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    client = Client()
    search_name = "Miley Cyrus" #only an example
    search = client.request("w/api.php?action=wbsearchentities&search="+search_name.replace(" ", "%20")+"&format=json&language=en&uselang=en&type=item")
    first_result = search["search"][0]
    entity = client.get(first_result["id"], load=True)

    # return will be defined later