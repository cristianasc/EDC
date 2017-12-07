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
import ssl


def home(request):
    db = Database()
    new_releases = db.get_new_releases()
    url_new_releases_images = db.get_new_releases_image()
    top_tracks = db.get_top_tracks()
    recently_played_by_user = db.get_recently_played_by_user()
    artist_info = db.get_artist_info()

    images = []
    news = []
    artists = []

    for image in url_new_releases_images:
        images += [image["url"]["value"]]

    for new in new_releases:
        news += [new["name"]["value"]]

    for artist in artist_info:
        artists += [[artist["name"]["value"],artist["image"]["value"],artist["followers"]["value"]]]

    if request.method == 'POST':
        artist = request.POST.get("search")
        search_artist(request,artist, artists)

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
                    'username': r["display_name"],
                    'photo': r["images"][0]["url"],
                    'new_releases': zip(news,images),
                    'top_tracks': top_tracks
                }
            )

        return render(
            request,
            'app/index.html',
            {
                'username': "",
                'new_releases': zip(news,images),
                'top_tracks': top_tracks
            }
        )

    except KeyError:
        return HttpResponseRedirect("/spotify_logout/")

def search_artist(request,artist, artists):
    db = Database()
    #token = request.COOKIES.get("SpotifyToken")
    #xmlString = db.getArtist(token,artist)
    #rdfartists = db.parse_artists(xmlString)
    #print(rdfartists)

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

def artist(request,id):
    try:
        """Verify if the user is logged in"""
        if request.COOKIES.get("SpotifyToken"):
            token = request.COOKIES.get("SpotifyToken")
            headers = {"Authorization": "Bearer " + token}
            r = requests.get('https://api.spotify.com/v1/artists/'+id, headers=headers)
            r = json.loads(r.text)

            wikidata_info = wikidata(r["name"])

            return render(
                request,
                'app/artistBio.html',
                {
                    'name': r["name"],
                    'image': r["images"][0]["url"],
                    'followers': r["followers"]["total"],
                    'wikidata': wikidata_info
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
                    'external_urls': r["external_urls"]["spotify"],
                    'birthdate': r["birthdate"],
                    'country': r["country"]
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


def wikidata(search_name):
    from SPARQLWrapper import SPARQLWrapper, JSON
    QUERY_URL = 'http://query.wikidata.org/sparql'

    """
        Override the SSL verification
    """
    ssl._create_default_https_context = ssl._create_unverified_context

    query = """
        SELECT ?p
        (SAMPLE(?name) as ?name) (SAMPLE(?birth) as ?birth) (SAMPLE(?facebook) as ?facebook) (SAMPLE(?twitter) as ?twitter)
        (SAMPLE(?instagram) as ?instagram) (SAMPLE(?url) as ?url) (SAMPLE(?official_site) as ?official_site)
        (SAMPLE(?country_name) as ?country_name)
        WHERE {
          ?p wdt:P106 wd:Q177220 .
          ?p rdfs:label ?name .
          OPTIONAL {?p wdt:P569 ?birth}
          OPTIONAL {?p wdt:P2013 ?facebook}
          OPTIONAL {?p wdt:P2002 ?twitter}
          OPTIONAL {?p wdt:P2003 ?instagram}
          OPTIONAL {?p wdt:P854 ?url}
          OPTIONAL {?p wdt:P856 ?official_site}
          OPTIONAL {?p wdt:P27 ?country .
                    ?country wdt:P1448 ?country_name}
          FILTER(REGEX(STR(?name), \"""" +search_name+ """.*$"))
        } GROUP BY ?p
        """

    sparql = SPARQLWrapper(QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)

    keys = [
        "birth",
        "facebook",
        "twitter",
        "instagram",
        "url",
        "official_site",
        "country_name"
    ]

    r = {}

    for key in keys:
        try:
            if len(results["results"]["bindings"]) > 0:
                r[key] = results["results"]["bindings"][0][key]["value"].replace("T00:00:00Z", "")
        except KeyError:
            continue

    return r

