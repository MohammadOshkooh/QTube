from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core', broker=settings.CELERY_BROKER_URL)
app.conf.worker_broker_connection_retry_on_startup = True

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.CELERY_BEAT_SCHEDULE = {

}

app.conf.CELERY_TIMEZONE = 'Asia/Tehran'
