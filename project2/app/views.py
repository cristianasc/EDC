from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
import spotipy
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
import json


def home(request):
    assert isinstance(request, HttpRequest)

    scope = "user-library-read"
    client_credentials_manager = SpotifyOAuth(client_id='e31546dc73154ddaab16538209d8526e',
                                              client_secret='f12c6904e491409bbc5834aaa86d14c0', scope=scope,
                                              redirect_uri='http://localhost:8000')
    if "code" in request.GET:
        code = request.GET.get("code")
        token = client_credentials_manager.get_access_token(code)

        print(token["access_token"])

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
