from .scrapers import get_lowest_performing, get_highest_performing
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from datetime import timedelta, time, date
from django.core.mail import send_mail
from .algos import z_score_analyzer
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
        stock = Decision.objects.latest('pk')
    except ObjectDoesNotExist:
        stock = None

    try:
        stocks = Decision.objects.all()
    except ObjectDoesNotExist:
        stocks = None

    d = { 'username': user.first_name, 'stock': stock, 'stocks': stocks}

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
    decisions = Decision.objects.filter(closingPrice=None)
    for decision in decisions:
        ticker = decision.stock.ticker
        tickDate = decision.tradeDate
        if timezone.now().date() > tickDate or timezone.now().time() > time(16,0,0):
            endDate = decision.tradeDate + timedelta(days=1)
            result = yf.Ticker(ticker).history(start=tickDate, end=endDate)
            closing = result["Close"].iloc[0]
            setattr(decision, "closingPrice", closing)
            decision.save()

def get_data(symbols):
    data = yf.download(symbols, period = "1y",interval = '1d' )
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
    if not Decision.objects.filter(tradeDate=last,algorithm=algo).exists():
        symbols = [x.ticker for x in stocks]
        if len(symbols) > 0:
            data = get_data(symbols)
            ticker, open, conf, tradeDate = z_score_analyzer(data, symbols)
            if tradeDate == last:
                stock = Stock.objects.get(ticker=ticker)
                Decision.objects.create(stock=stock,algorithm=algo, openPrice=open, confidence=conf, tradeDate=tradeDate, long=True)

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
    highest = get_highest_performing()
    lowest = get_lowest_performing()
    algo1 = Algorithm.objects.create(name="Buy previous day's biggest gainer")
    algo2 = Algorithm.objects.create(name="Buy previous day's biggest loser")
    stock1 = Stock.objects.get_or_create(ticker=highest.upper())[0]
    stock2 = Stock.objects.get_or_create(ticker=lowest.upper())[0]
    Decision.objects.create(stock=stock1,algorithm=algo1,tradeDate=last,long=True)
    Decision.objects.create(stock=stock2,algorithm=algo2,tradeDate=last,long=True)