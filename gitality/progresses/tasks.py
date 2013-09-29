from celery.task import periodic_task
from celery.task.schedules import crontab

from .models import ProjectProgress


@periodic_task(run_every=crontab(hour='*', minute='*/15', day_of_week='*'))
def update_projects_state():
    progresses = ProjectProgress.objects.all()
    for progress in progresses:
        progress.update_state()
