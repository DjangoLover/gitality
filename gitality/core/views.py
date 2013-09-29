from django.shortcuts import render

from .exceptions import DeliberateError


def home(request):
    return render(request, 'core/index.html')


def login(request):
    return render(request, 'core/login.html')


def error(request):
    raise DeliberateError('Social auth error')
