from django.shortcuts import render

from .exceptions import DeliberateError


def home(request):
    context = {

    }
    return render(request, 'core/index.html', context)


def login(request):
    return render(request, 'core/login.html')


def error(request):
    raise DeliberateError('Social auth error')
