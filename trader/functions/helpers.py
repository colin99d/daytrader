from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.core.mail import send_mail
from datetime import timedelta, time
from .algos import z_score_analyzer
from django.utils import timezone
from datetime import datetime
import yfinance as yf
import requests, re


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

def get_cashflows(ticker, quarterly=False):
    ending = "cashflowStatementHistory" if quarterly == False else "cashflowStatementHistoryQuarterly"
    url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ ticker.upper() +'?modules='+ending
    response = requests.get(url).json()
    items = response['quoteSummary']['result'][0][ending]['cashflowStatements']
    dictVals = [{"id": "Operating Cash Flows", "data": []},{"id": "Financing Cash Flows", "data": []},{"id": "Investing Cash Flows", "data": []}]
    for item in items:
        date = datetime.utcfromtimestamp(item['endDate']['raw']).strftime("%m-%d-%Y")
        dictVals[0]["data"].append({"x":date,"y":item['totalCashFromOperatingActivities']['raw']})
        dictVals[1]["data"].append({"x":date,"y":item['totalCashFromFinancingActivities']['raw']})
        dictVals[2]["data"].append({"x":date,"y":item['totalCashflowsFromInvestingActivities']['raw']})    
    return dictVals

def valid_ticker(symbol):
    url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ symbol.upper() +'?modules=price'
    response = requests.get(url).content.decode('utf-8')
    ticker = re.search('price', response)
    return False if ticker == None else True

def last_date(dt):
    weekday = dt.weekday()
    currTime = dt.time()
    if weekday == 5:
        lastDate = (dt - timedelta(days=1)).date()
        close = True
    elif weekday == 6:
        lastDate = (dt - timedelta(days=2)).date()
        close = True
    else:
        if currTime > time(16,0,0):
            lastDate = dt.date()
            close = True
        elif currTime > time(9,30,0):
            lastDate = dt.date()
            close = False
        else:
            lastDate = (dt - timedelta(days=1)).date()
            close = True
    return lastDate, close

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

def get_stock(algo):
    from trader.models import Stock, Decision
    last = last_date(timezone.now())[0]
    if not Decision.objects.filter(tradeDate=last,algorithm=algo).exists():
        symbols = [x.ticker for x in Stock.objects.all()]
        data = get_data(symbols)
        ticker, open, conf, tradeDate = z_score_analyzer(data, symbols)
        stock = Stock.objects.get(ticker=ticker)
        Decision.objects.create(stock=stock,algorithm=algo,openPrice=open,confidence=conf, tradeDate=tradeDate)