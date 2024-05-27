import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_d3.settings')

app = Celery('news_d3')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_digit_5_seconds': {
        'task': 'tasks.digit',
        'schedule': 5,
        'args': (5, 2)
    }
}

