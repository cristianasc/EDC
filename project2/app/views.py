from django.shortcuts import render
from django.http import HttpRequest
from django.utils.datastructures import MultiValueDictKeyError
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
import spotipy
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
from .models.models import Database
import requests
import json
from .models.queries import search_artist_info, search_artist_relationships, search_artist_genre, \
    search_artist_occupations
import random
import string
import uuid


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

            #db.new_releases(token)
            #$db.top_tracks(token)


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


def generate(request):
    token = request.COOKIES.get("SpotifyToken")
    Database.getArtistTop(token=token)
    db = Database()
    return HttpResponse(content=b"Done")


def search(request):
    try:
        if request.COOKIES.get("SpotifyToken"):
            text = request.POST["text"]

            db = Database()
            search_artists = db.search_artists(name=text)
            search_musics_and_albums = db.search_musics_and_albums(name=text)

            if isinstance(search_artists, dict):
                search_artists = [search_artists]

            if isinstance(search_musics_and_albums, dict):
                search_musics_and_albums = [search_musics_and_albums]

            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}

            # get musics from spotify
            url = "https://api.spotify.com/v1/search?q="+text+"&type=track&limit=10"
            r_musics = requests.get(url, headers=headers)
            r_musics = json.loads(r_musics.text)

            for row in r_musics["tracks"]["items"]:
                if not any(d['name'] == row["name"] for d in search_musics_and_albums):
                    search_musics_and_albums.append({"name": row["name"], "id": row["id"]})

            # get albuns from spotify
            url = "https://api.spotify.com/v1/search?q="+text+"&type=album&limit=10"
            r_musics = requests.get(url, headers=headers)
            r_musics = json.loads(r_musics.text)

            for row in r_musics["albums"]["items"]:
                if not any(d['name'] == row["name"] for d in search_musics_and_albums):
                    search_musics_and_albums.append({"name": row["name"], "id": row["id"]})

            # get artist from spotify
            url = "https://api.spotify.com/v1/search?q="+text+"&type=artist&limit=10"
            r_musics = requests.get(url, headers=headers)
            r_musics = json.loads(r_musics.text)

            for row in r_musics["artists"]["items"]:
                if not any(d['nameartist'] == row["name"] for d in search_artists):
                    search_artists.append({"nameartist": row["name"], "artist_id": row["id"]})

            # get username etc
            r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            r = json.loads(r.text)

            return render(
                request,
                'app/search.html',
                {
                    'title': text,
                    'username': r["display_name"],
                    'photo': r["images"][0]["url"],
                    'artists': search_artists,
                    'musics_and_albums': search_musics_and_albums,
                    'text': text
                }
            )
        else:
            return HttpResponseRedirect("/login/")

    except MultiValueDictKeyError:
        return HttpResponseRedirect("/")



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

            r_artist_top_tracks = requests.get('https://api.spotify.com/v1/artists/'+id+'/top-tracks?country=PT', headers=headers)
            r_artist_top_tracks = json.loads(r_artist_top_tracks.text)

            if isinstance(artist_rel, dict):
                for key, value in artist_rel.items():
                    if (key == "sibling" or key == "occupations") and isinstance(value, str):
                        artist_rel[key] = [value]

            if isinstance(artist_occupations, dict):
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
                    'artist_occupations': artist_occupations,
                    'artist_top_tracks': r_artist_top_tracks["tracks"]
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

def music(request, id):
    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            # search in db top_tracks
            db = Database()
            result = db.get_music_info(id, request.COOKIES.get("SpotifyToken"))
            global music_id
            music_id = id

            comments = db.get_comments(id)

            ids = result["artists_ids"]
            artists = result["artists"]

            del result["artists_ids"]

            if isinstance(ids, str):
                ids = [ids]

            if isinstance(artists, str):
                artists = [artists]

            if isinstance(comments, dict):
                comments = [comments]

            result["artists"] = list(zip(artists, ids))
            url = result["external_urls"].replace("https://open.spotify.com/", "").split("/")
            result["uri"] = "spotify:"+url[0]+":"+url[1]

            # get user name and photo
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            user_r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            user_r = json.loads(user_r.text)

            for i in range(0, len(comments)):
                comments[i]["comment_id"] = comments[i]["comment_id"].split("/")[-1]

            return render(
                request,
                'app/music.html',
                {
                    'username': user_r["display_name"],
                    'photo': user_r["images"][0]["url"],
                    'user': user_r["id"],
                    "music": result,
                    "music_id": id,
                    "comments": comments
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

    scope = "user-read-private user-read-birthdate user-read-recently-played user-read-playback-state user-follow-read playlist-read-collaborative user-top-read"
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

            # Get a User’s Available Devices
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r_devices = requests.get('https://api.spotify.com/v1/me/player/devices', headers=headers)
            r_devices = json.loads(r_devices.text)

            # Get the User’s Currently Playing Track
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r_currently_playing = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
            r_currently_playing = json.loads(r_currently_playing.text)

            # Get the User’s following list
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r_following = requests.get('https://api.spotify.com/v1/me/following?type=artist',
                                               headers=headers)
            r_following = json.loads(r_following.text)

            # Get the User’s playlists
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r_playlists = requests.get('https://api.spotify.com/v1/me/playlists',
                                       headers=headers)
            r_playlists = json.loads(r_playlists.text)

            return render(request, 'app/account.html',
                {
                    'username': r["display_name"],
                    'photo': r["images"][0]["url"],
                    'followers': r["followers"]["total"],
                    'id': r["id"],
                    'external_urls': r["external_urls"]["spotify"],
                    'birthdate': r["birthdate"],
                    'country': r["country"],
                    'musics': musics[:10],
                    'devices': r_devices["devices"],
                    'currently_playing': r_currently_playing["item"],
                    'following': r_following["artists"]["items"],
                    'playlists': r_playlists["items"]
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

def comments(request):
    db = Database()
    try:
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            user_r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            user_r = json.loads(user_r.text)

            name = user_r["display_name"]
            user_id = user_r["id"]
            comment_id = str(uuid.uuid4())

            db.comment(user_id, name, request.POST["comment"], request.POST["music_id"], comment_id)

            return render(
                request,
                'app/music.html',
                {
                    'data': ""
                }
            )

        return render(
            request,
            'app/music.html',
            {
                'data': ""
            }
        )

    except KeyError:
        return HttpResponseRedirect("/spotify_logout/")

def delete(request):
    db = Database()
    try:
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            user_r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            user_r = json.loads(user_r.text)

            name = user_r["display_name"]
            user_id = user_r["id"]


            if request.method == 'POST':
                uid = request.POST.get("uid")
                comment_id = request.POST.get("comment_id")
                db.delcomment(user_id, name, uid, comment_id)

            return render(
                request,
                'app/music.html',
                {
                    'data': ""
                }
            )

        return render(
            request,
            'app/music.html',
            {
                'data': ""
            }
        )

    except KeyError:
        return HttpResponseRedirect("/spotify_logout/")

def statistics(request):
    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            # search in db top_tracks
            db = Database()

            # get user name and photo
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            user_r = requests.get('https://api.spotify.com/v1/me', headers=headers)
            user_r = json.loads(user_r.text)

            # query platform data
            platform_data = db.platform_data()
            top_followers = db.get_best_followers()

            return render(
                request,
                'app/statistics.html',
                {
                    'title': 'Statistics',
                    'username': user_r["display_name"],
                    'photo': user_r["images"][0]["url"],
                    'platform_data': platform_data,
                    'top_followers' : top_followers
                }
            )

        return render(
            request,
            'app/statistics.html',
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

