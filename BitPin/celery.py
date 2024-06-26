# BitPin/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BitPin.settings')

app = Celery('BitPin')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'detect-fraudulent-reviews-every-7-days': {
        'task': 'content.tasks.detect_fraudulent_reviews.detect_fraudulent_reviews',
        'schedule': timedelta(days=7),
    },
}
