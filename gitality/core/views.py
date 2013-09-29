from django.shortcuts import render

from .exceptions import DeliberateError
from achievements.models import (
    CommitAuthorAchievement,
    CommitAchievement,
    ProjectAchievement)


def home(request):
    latest_comitauthor = CommitAuthorAchievement.objects.order_by('created')
    # latest_comit = CommitAchievement.objects.order_by('created')
    latest_proj = ProjectAchievement.objects.order_by('created')
    context = {
        'latest_comitauthor': latest_comitauthor[:20],
        # 'latest_comit': latest_comit[:20],
        'latest_proj': latest_proj[:20],
    }
    return render(request, 'core/index.html', context)


def login(request):
    return render(request, 'core/login.html')


def error(request):
    raise DeliberateError('Social auth error')
