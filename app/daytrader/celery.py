from celery.schedules import crontab
from django.core import serializers
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daytrader.settings')

app = Celery('daytrader')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

#Helper tasks that are called by main tasks
@app.task(serializer='json')
def send_email(algo):
    from trader.functions.helpers import daily_email
    from trader.models import Algorithm
    from user.models import User
    algo = Algorithm.objects.get(pk=algo)
    for item in User.objects.filter(daily_emails=True,selected_algo=algo):
        if item.email:
            daily_email(item)

celery_send_email = send_email.s()

@app.task(serializer='json')
def get_open():
    from trader.functions.helpers import get_opening
    get_opening()

get_open_price = get_open.s()

#Main tasks
@app.task(serializer='json')
def begin_day(n):
    from trader.functions.helpers import get_stock
    from trader.models import Decision, Algorithm, Stock
    algo = Algorithm.objects.get_or_create(name="Z-score daytrader",public=True)
    stocks = Stock.objects.filter(price__lt=100, price__gt=0,listed=True).order_by('-volume')[:n]
    get_stock(algo[0], stocks)
    celery_send_email(algo[0].pk)
    get_open_price()
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

@app.task(serializer='json')
def get_high_and_low():
    from trader.models import Decision, Algorithm
    from trader.functions.helpers import get_highest_lowest
    get_highest_lowest()
    algo1 = Algorithm.objects.get(name="Buy previous day's biggest gainer")
    algo2 = Algorithm.objects.get(name="Buy previous day's biggest loser")
    celery_send_email(algo1.pk)
    celery_send_email(algo2.pk)
    return serializers.serialize('json', Decision.objects.all())



@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    #Decide which stocks to buy (using original algo) and send a mass mail every weekday at 9:32 am
    sender.add_periodic_task(crontab(hour=9, minute=32, day_of_week='1-5'), begin_day.s(50), name='Get daily trade')
    #Get closing prices for all stocks at 4:01 pm every weekday
    sender.add_periodic_task(crontab(hour=16, minute=1, day_of_week='1-5'), end_day.s(), name='Get closing price')
    #Update list of all stocks every Friday at 5 pm
    sender.add_periodic_task(crontab(hour=17, minute=0, day_of_week='5'), get_stock_tickers.s(), name='Get all NYSE and NASDAQ tickers')
    #Spend Friday night to Monday morning getting new stock information
    sender.add_periodic_task(crontab(hour='*', minute=0, day_of_week='6,0'), get_stock_info.s(150), name='Update information for tickers')
    #Get the biggest gainer and loser from the previous day
    sender.add_periodic_task(crontab(hour='17', minute=0, day_of_week='1-5'), get_high_and_low.s(), name='Get biggest gainer and loser')
    