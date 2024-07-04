from celery import Celery

app = Celery("freelancer_platform")
app.config_from_object("django.conf.settings", namespace="CELERY")
app.autodiscover_tasks()
