import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")

app = Celery("library_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-overdue-notifications-everyday": {
        "task": "borrowing.tasks.send_overdue_notification",
        "schedule": crontab(hour=21, minute=30),
    },
}

