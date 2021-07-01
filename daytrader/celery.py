from trader.functions import today_trade, get_closing, daily_email
from celery.schedules import crontab
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daytrader.settings')

app = Celery('daytrader')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

@app.task
def begin_day():
    from trader.models import Decision, Algorithm
    from user.models import User
    algo = Algorithm.objects.get_or_create(name="Z-score daytrader",public=True)
    today_trade(algo[0])
    for item in User.objects.all():
        if item.email:
            daily_email(item)
    return Decision.objects.all()

@app.task
def end_day():
    from trader.models import Decision
    get_closing()
    return Decision.objects.all()

@app.task
def send_email():
    from user.models import User
    for item in User.objects.all():
        if item.email:
            daily_email(item)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=9, minute=32, day_of_week='1-5'), begin_day, name='Get daily trade')
    sender.add_periodic_task(crontab(hour=16, minute=1, day_of_week='1-5'), end_day, name='Get closing price')
