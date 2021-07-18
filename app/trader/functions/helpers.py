from .scrapers import get_lowest_performing, get_highest_performing
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from datetime import timedelta, time, date
from django.core.mail import send_mail
from .algos import z_score_analyzer
from .scrapers import valid_ticker
from django.utils import timezone
from .scrapers import get_tickers
from django.db.models import F, Q
from trader.models import Stock
import yfinance as yf


def daily_email(user):
    from trader.models import Decision
    subject, from_email, to = 'Daily Stock Pick', 'cdelahun@iu.edu', user.email
    text= get_template('email/email.txt')
    html = get_template('email/email.html')

    try:
        stock = Decision.objects.filter(algorithm=user.selected_algo).latest('pk')
    except ObjectDoesNotExist:
        stock = None

    try:
        stocks = Decision.objects.filter(algorithm=user.selected_algo)
    except ObjectDoesNotExist:
        stocks = None

    d = {'username': user.first_name, 'stock': stock, 'stocks': stocks, 'algorithm':user.selected_algo}

    text_content = text.render(d)
    html_content = html.render(d)

    send_mail(subject,text_content,from_email,[to],html_message=html_content, fail_silently=False)


def last_date(dt):
    holidays = [date(2021,7,5),date(2021,9,6),date(2021,12,24),date(2022,1,17),date(2022,2,21),date(2022,4,15),date(2022,5,30),date(2022,7,4),
        date(2022,9,5),date(2022,12,26),date(2023,1,2),date(2023,1,16),date(2023,2,20),date(2023,4,7),date(2023,5,29),date(2023,7,4),
        date(2023,9,4),date(2023,12,25)]
    if dt.date() in holidays:
        dt = dt - timedelta(days=1)
    weekday = dt.weekday()
    currTime = dt.time()
    if weekday == 5:
        lastDate = (dt - timedelta(days=1)).date()
        nextDate = (dt + timedelta(days=2)).date()
        close = True
    elif weekday == 6:
        lastDate = (dt - timedelta(days=2)).date()
        nextDate = (dt + timedelta(days=1)).date()
        close = True
    else:
        if currTime > time(16,0,0):
            lastDate = dt.date()
            nextDate = (dt + timedelta(days=1)).date()
            close = True
        elif currTime > time(9,30,0):
            lastDate = dt.date()
            nextDate = dt.date()
            close = False
        else:
            lastDate = (dt - timedelta(days=1)).date()
            nextDate = dt.date()
            close = True
    return lastDate, close, nextDate

def get_closing():
    from trader.models import Decision
    decisions = Decision.objects.filter(closing_price=None)
    for decision in decisions:
        ticker = decision.stock.ticker
        tickDate = decision.trade_date
        if timezone.now().date() > tickDate or timezone.now().time() > time(16,0,0):
            endDate = decision.trade_date + timedelta(days=1)
            result = yf.Ticker(ticker).history(start=tickDate, end=endDate)
            closing = result["Close"].iloc[0]
            setattr(decision, "closing_price", closing)
            decision.save()

def get_opening():
    from trader.models import Decision
    decisions = Decision.objects.filter(open_price=None)
    for decision in decisions:
        ticker = decision.stock.ticker
        tickDate = decision.trade_date
        if timezone.now().date() > tickDate or timezone.now().time() > time(16,0,0):
            endDate = decision.trade_date + timedelta(days=1)
            result = yf.Ticker(ticker).history(start=tickDate, end=endDate)
            opening = result["Open"].iloc[0]
            setattr(decision, "open_price", opening)
            decision.save()

def get_data(symbols):
    data = yf.download(symbols, period = "1y",interval = '1d')
    for symbol in symbols:
        data['pHigh',symbol] = data['High',symbol].shift(1)
        data['pLow',symbol] = data['Low',symbol].shift(1)
        data['pClose',symbol] = data['Close',symbol].shift(1)
        data['pVolume',symbol] = data['Volume',symbol].shift(1)
        data = data.iloc[1:]
        data = data.fillna(0)
    return data

def get_stock(algo, stocks):
    from trader.models import Stock, Decision
    last = last_date(timezone.now())[0]
    if not Decision.objects.filter(trade_date=last,algorithm=algo).exists():
        symbols = [x.ticker for x in stocks if valid_ticker(x.ticker)]
        if len(symbols) > 0:
            data = get_data(symbols)
            ticker, open, conf, trade_date = z_score_analyzer(data, symbols)
            if trade_date == last:
                stock = Stock.objects.get(ticker=ticker)
                Decision.objects.create(stock=stock,algorithm=algo, open_price=open, confidence=conf, trade_date=trade_date, long=True)

def get_stocklist_html():
    nasdaq = get_tickers("NASDAQ")
    nyse = get_tickers("NYSE")
    stocks = nasdaq + nyse
    for stock in stocks:
        item = Stock.objects.get_or_create(ticker=stock["ticker"])[0]
        setattr(item,"name",stock["name"])
        setattr(item,"exchange",stock["exchange"])
        item.save()

def get_stock_data(stocks, n):
    newList = stocks.filter(~Q(listed=False)).order_by(F('last_updated').asc(nulls_first=True))[:n]
    for item in newList:
        if item.last_updated is None:
            item.update_stock_info()
        elif (timezone.now() - item.last_updated) > timedelta(days=6):
            item.update_stock_info()

def get_highest_lowest():
    from trader.models import Decision, Stock, Algorithm
    last = last_date(timezone.now())[2]
    algo1 = Algorithm.objects.get_or_create(name="Buy previous day's biggest gainer")[0]
    algo2 = Algorithm.objects.get_or_create(name="Buy previous day's biggest loser")[0]
    if not Decision.objects.filter(trade_date=last,algorithm=algo1).exists():
        highest = get_highest_performing()
        stock1 = Stock.objects.get_or_create(ticker=highest.upper())[0]
        Decision.objects.create(stock=stock1,algorithm=algo1,trade_date=last,long=True)
    
    if not Decision.objects.filter(trade_date=last,algorithm=algo2).exists():
        lowest = get_lowest_performing()
        stock2 = Stock.objects.get_or_create(ticker=lowest.upper())[0]
        Decision.objects.create(stock=stock2,algorithm=algo2,trade_date=last,long=True)