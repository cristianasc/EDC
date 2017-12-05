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


def home(request):
    db = Database()
    new_releases = db.get_new_releases()
    url_new_releases_images = db.get_new_releases_image()
    top_tracks = db.get_top_tracks()
    top_tracks_artists = db.get_top_tracks_artists()


    images = []
    news = []
    toptracks_names = []
    toptracks_images = []
    toptracks_artists = []
    tt_names = []

    for image in url_new_releases_images:
        images += [image["url"]["value"]]

    for new in new_releases:
        news += [new["name"]["value"]]

    for toptracks_name in top_tracks:
        toptracks_names += [toptracks_name["name"]["value"]]
        toptracks_images += [toptracks_name["src"]["value"]]

    for top_tracks_artist in top_tracks_artists:
        tt_names += [top_tracks_artist["name"]["value"]]
        toptracks_artists += [top_tracks_artist["nameartist"]["value"]]

    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            r = json.loads(r.text)
            print(r)

            return render(
                request,
                'app/index.html',
                {
                    'username': r["display_name"],
                    'photo': r["images"][0]["url"],
                    'new_releases': zip(news,images),
                    'top_tracks': zip(toptracks_names,toptracks_images),
                    'artists':zip(toptracks_artists,tt_names)
                }
            )

        return render(
            request,
            'app/index.html',
            {
                'username': "",
                'new_releases': zip(news,images),
                'top_tracks': zip(toptracks_names,toptracks_images),
                'artists': zip(toptracks_artists,tt_names)
            }
        )

    except KeyError:
        return HttpResponseRedirect("/spotify_logout/")


def new_releases(request):
    db = Database()
    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")

            db.new_releases(token)

            return render(
                request,
                'app/index.html',
                {
                    'data': ""
                }
            )

        return render(
            request,
            'app/account.html',
            {
                'username': "",
            }
        )
    except:
        return HttpResponseRedirect("/spotify_logout/")

def top_tracks(request):
    db = Database()
    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")

            db.top_tracks(token)

            return render(
                request,
                'app/index.html',
                {
                    'data': ""
                }
            )
        return render(
            request,
            'app/account.html',
            {
                'username': "",
            }
        )

    except:
        return HttpResponseRedirect("/spotify_logout/")

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

    scope = "user-read-private user-read-birthdate user-read-recently-played"
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


def user_account(request):

    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            r = json.loads(r.text)
            print(r)
            Database().recently_played_by_user(token)


            return render(
                request,
                'app/account.html',
                {
                    'username': r["display_name"],
                    'photo': r["images"][0]["url"],
                    'followers': r["followers"]["total"],
                    'id': r["id"],
                    'external_urls': r["external_urls"]["spotify"]
                }
            )

        return render(
            request,
            'app/account.html',
            {
                'username': "",
            }
        )

    except KeyError:
        return HttpResponseRedirect("/spotify_logout/")


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