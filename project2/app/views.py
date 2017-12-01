from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegistrationForm
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect


def home(request):
    assert isinstance(request, HttpRequest)

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
