import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregator.settings')
app = Celery('aggregator', broker='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'save-news-every-1-min': {
        'task': 'news.views.save_news',
        'schedule': crontab(minute=1),
    },
    'test': {
        'task': 'celery.debug_task',
        'schedule': 5.0,
    },
}
app.conf.timezone = 'UTC'
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
