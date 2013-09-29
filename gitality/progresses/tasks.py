from celery import task

from .models import ProjectProgress


@task
def update_projects_state():
    progresses = ProjectProgress.objects.all()
    for progress in progresses:
        progress.update_state()
