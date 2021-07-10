from celery.schedules import crontab
from django.core import serializers
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daytrader.settings')

app = Celery('daytrader')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

@app.task(serializer='json')
def begin_day(n):
    from trader.functions.helpers import daily_email, get_stock
    from trader.models import Decision, Algorithm, Stock
    from user.models import User
    algo = Algorithm.objects.get_or_create(name="Z-score daytrader",public=True)
    stocks = Stock.objects.filter(price__lt=100, price__gt=0,listed=True).order_by('-volume')[:n]
    get_stock(algo[0], stocks)
    for item in User.objects.all():
        if item.email:
            daily_email(item)
    return serializers.serialize('json', Decision.objects.all())

@app.task(serializer='json')
def end_day():
    from trader.functions.helpers import get_closing
    from trader.models import Decision
    get_closing()
    return serializers.serialize('json', Decision.objects.all())

@app.task(serializer='json')
def get_stock_tickers():
    from trader.functions.helpers import get_stocklist_html
    from trader.models import Stock
    get_stocklist_html()
    return serializers.serialize('json', Stock.objects.all())

@app.task(serializer='json')
def get_stock_info(n):
    from trader.functions.helpers import get_stock_data
    from trader.models import Stock
    get_stock_data(Stock.objects.all(), n)
    return serializers.serialize('json', Stock.objects.all())


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #Decide which stocks to buy (using original algo) and send a mass mail every weekday at 9:32 am
    sender.add_periodic_task(crontab(hour=9, minute=32, day_of_week='1-5'), begin_day.delay(50), name='Get daily trade')
    #Get closing prices for all stocks at 4:01 pm every weekday
    sender.add_periodic_task(crontab(hour=16, minute=1, day_of_week='1-5'), end_day.delay(), name='Get closing price')
    #Update list of all stocks every Friday at 5 pm
    sender.add_periodic_task(crontab(hour=17, minute=0, day_of_week='5'), get_stock_tickers.delay(), name='Get all NYSE and NASDAQ tickers')
    #Spend Friday night to Monday morning getting new stock information
    sender.add_periodic_task(crontab(hour='*', minute=0, day_of_week='6,0'), get_stock_info.delay(150), name='Update information for tickers')

