from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
import spotipy
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
from .models.models import Database
import requests
import json
from .models.queries import search_artist_info, search_artist_relationships, search_artist_genre, \
    search_artist_occupations


def home(request):
    db = Database()
    new_releases = db.get_new_releases()
    top_tracks = db.get_top_tracks()

    # new releases
    tmp = new_releases
    new_releases = []

    for new_release in tmp:
        artists = new_release["artists"]
        if isinstance(artists, str):
            artists = [artists]

        ids = new_release["ids"]
        if isinstance(ids, str):
            ids = [ids]

        del new_release["ids"]
        new_release["artists"] = list(zip(artists, ids))

        new_releases.append(new_release)


    # top tracks
    tmp = top_tracks
    top_tracks = []

    for top_track in tmp:
        artists = top_track["artists"]
        if isinstance(artists, str):
            artists = [artists]

        ids = top_track["ids"]
        if isinstance(ids, str):
            ids = [ids]

        del top_track["ids"]
        top_track["artists"] = list(zip(artists, ids))

        top_tracks.append(top_track)

    try:
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
                    'title': "Home",
                    'username': r["display_name"],
                    'photo': r["images"][0]["url"],
                    'new_releases': new_releases,
                    'top_tracks': top_tracks
                }
            )

        return render(
            request,
            'app/index.html',
            {
                'title': "Home",
                'username': "",
                'new_releases': new_releases,
                'top_tracks': []
            }
        )

    except KeyError:
        return HttpResponseRedirect("/spotify_logout/")


def search_artist(request,artist, artists):
    db = Database()

    for i in artists:
        if artist == i[0]:
            print(i[0],i[1],i[2])

    return render(
        request,
        'app/index.html',
        {
            'data': ""
        }
    )


def artist(request, id):
    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r = requests.get('https://api.spotify.com/v1/artists/'+id, headers=headers)
            r = json.loads(r.text)

            artist_info = search_artist_info(r["name"])
            try:
                artist_rel = search_artist_relationships(artist_info["p"])
                artist_genre = search_artist_genre(artist_info["p"])
                artist_occupations = search_artist_occupations(artist_info["p"])
            except TypeError:
                artist_rel = []
                artist_genre = []
                artist_occupations = []

            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            user_r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            user_r = json.loads(user_r.text)

            for key, value in artist_rel.items():
                if (key == "sibling" or key == "occupations") and isinstance(value, str):
                    artist_rel[key] = [value]

            for key, value in artist_occupations.items():
                if (key == "occupations") and isinstance(value, str):
                    artist_occupations[key] = [value]

            return render(
                request,
                'app/artistBio.html',
                {
                    'username': user_r["display_name"],
                    'photo': user_r["images"][0]["url"],
                    'title': r["name"],
                    'name': r["name"],
                    'image': r["images"][0]["url"],
                    'followers': r["followers"]["total"],
                    'artist_info': artist_info,
                    'artist_rel': artist_rel,
                    'artist_genre': artist_genre,
                    'artist_occupations': artist_occupations
                }
            )

        return render(
            request,
            'app/artistBio.html',
            {
                'username': "",
            }
        )

    except KeyError:
        return HttpResponseRedirect("/spotify_logout/")


def music(request, id):
    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            # search in db top_tracks
            db = Database()
            result = db.get_music_info(id)

            ids = result["artists_ids"]
            artists = result["artists"]

            del result["artists_ids"]

            if isinstance(ids, str):
                ids = [ids]

            if isinstance(artists, str):
                artists = [artists]

            result["artists"] = list(zip(artists, ids))
            url = result["external_urls"].replace("https://open.spotify.com/", "").split("/")
            result["uri"] = "spotify:"+url[0]+":"+url[1]

            # get user name and photo
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            user_r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            user_r = json.loads(user_r.text)

            return render(
                request,
                'app/music.html',
                {
                    'username': user_r["display_name"],
                    'photo': user_r["images"][0]["url"],
                    "music": result,
                    "music_id": id
                }
            )

        return render(
            request,
            'app/index.html',
            {
                'username': "",
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
            musics = Database().get_recently_played_by_user()

            return render(request, 'app/account.html',
                {
                    'username': r["display_name"],
                    'photo': r["images"][0]["url"],
                    'followers': r["followers"]["total"],
                    'id': r["id"],
                    'external_urls': r["external_urls"]["spotify"],
                    'birthdate': r["birthdate"],
                    'country': r["country"],
                    'musics': musics[:10]
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


def get_top_tracks_by_user(request):
    pass


def spotify_logout(request):
    assert isinstance(request, HttpRequest)

    response = HttpResponseRedirect("/")
    response.delete_cookie("SpotifyToken")

    return response

