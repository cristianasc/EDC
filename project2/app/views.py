from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
import spotipy
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
import json
import requests


def home(request):
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
    print(r.text)

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
