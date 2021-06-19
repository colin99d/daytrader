from trader.functions import today_trade, get_closing
from celery.schedules import crontab
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daytrader.settings')


# Celery app
app = Celery('daytrader')

app.config_from_object('django.conf:settings')

# Autodiscover <app>.tasks.py
app.autodiscover_tasks()


# This is a debug task
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def begin_day():
    today_trade()

@app.task
def end_day():
    get_closing()

@app.task
def hello():
    print('hello')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, hello, name='add every 10')

    sender.add_periodic_task(crontab(hour=9, minute=31, day_of_week='1-5'), begin_day, name='Get daily trade')

    sender.add_periodic_task(crontab(hour=16, minute=1, day_of_week='1-5'), end_day, name='Get closing price')
