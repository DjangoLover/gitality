from django.shortcuts import render

from .exceptions import DeliberateError
from commits.models import Commit


def home(request):
    # Place unlocked achievements here
    lately_unlocked = Commit.objects.order_by('-last_modified')
    context = {
        'lately_unlocked': lately_unlocked[:25],
        # 'added_achievements': 'blah'
    }
    return render(request, 'core/index.html', context)


def login(request):
    return render(request, 'core/login.html')


def error(request):
    raise DeliberateError('Social auth error')
