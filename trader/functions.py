from django.core.exceptions import ObjectDoesNotExist
from sklearn.model_selection import train_test_split
from django.template.loader import get_template
from django.core.mail import send_mail
from datetime import timedelta, time
from django.utils import timezone
from sklearn import linear_model
import scipy.stats as scpy
import yfinance as yf
import pandas as pd
import requests, re
import numpy as np

def last_date(dt):
    weekday = dt.weekday()
    currTime = dt.time()
    if weekday == 5:
        lastDate = (timezone.now() - timedelta(days=1)).date()
        close = True
    elif weekday == 6:
        lastDate = (timezone.now() - timedelta(days=2)).date()
        close = True
    else:
        if currTime > time(16,0,0):
            lastDate = timezone.now().date()
            close = True
        elif currTime > time(9,30,0):
            lastDate = timezone.now().date()
            close = False
        else:
            lastDate = (timezone.now() - timedelta(days=1)).date()
            close = True
    return lastDate, close


def valid_ticker(symbol):
    url = 'https://finance.yahoo.com/quote/' + symbol.upper()
    response = requests.get(url).content.decode('utf-8')
    ticker = re.search('Previous Close', response)
    return False if ticker.start() > 200000 else True

def today_trade():
    from .models import Algorithm, Stock, Decision
    last = last_date(timezone.now())
    if last not in [x.tradeDate.date() for x in Decision.objects.all()]:
        symbols = [x.ticker for x in Stock.objects.all()]
        data = get_data(symbols)
        ticker, open, conf, tradeDate = get_pick(data, symbols)
        stock = Stock.objects.get(ticker=ticker)
        try:
            algo = Algorithm.objects.get(pk=1)
        except:
            algo = Algorithm.objects.create(name="First Algo")
        Decision.objects.create(stock=stock,algorithm=algo,openPrice=open,confidence=conf, tradeDate=tradeDate)

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

def get_pick(data, symbols):
    opens = []
    closes = []
    decisions = []
    
    for symbol in symbols:
        x=0
        y=-2
        z=-1
        #features = ['Open','pHigh','pLow','pClose','pVolume']
        #symbolz = [x for symbol in features]
        #X = data[features, symbolz][i+1:i+64]
        X = data['Open', symbol][x:y].to_numpy().reshape(-1,1)
        y = data['Close',symbol][x:y]
            
        #Split data into train and test
        train_X, val_X, train_y, val_y = train_test_split(X, y)
        
        #Create model and predictions
        model = linear_model.LinearRegression()
        model.fit(train_X, train_y)
        preds_val = model.predict(val_X)
            
        #Compute stock 95% confidence interval
        l1 = preds_val - val_y
        mean = np.average(l1)
        stdev = np.std(l1)
        predict = data['Open',symbol][z].reshape(1,-1)
        pred_increase = model.predict(predict)- data['Open',symbol][z]

        #Compute long/short with confidence 
        zscore = 3
        while True:
            lowf = mean - zscore*stdev + pred_increase
            highf = mean + zscore*stdev + pred_increase
                
            if lowf > 0 and highf > 0:
                prob = scpy.norm.sf(abs(zscore))*2
                prob = 1 - prob
                decision = round(prob*100,2)
                break
                
            elif lowf < 0 and highf < 0:
                prob = scpy.norm.sf(abs(zscore))*2
                prob = 1 - prob
                decision = round(prob*100,2) *-1
                break 
                
            else:
                zscore -= .001

        #Add data to lists
        opens.append(data['Open',symbol][z])
        closes.append(data['Close',symbol][z])
        decisions.append(decision)
        
    #Turn lists into a Dataframe 
    df = pd.DataFrame({'ticker': symbols,'date': data.index[z],'open': opens,'decision': decisions,'close':closes})
    df_sorted = df.sort_values(by=['decision']).reset_index()
    long = df_sorted['ticker'][len(df_sorted)-1]
    #longs = [df_sorted['date'][len(df_sorted)-1],df_sorted['ticker'][len(df_sorted)-1],df_sorted['open'][len(df_sorted)-1],df_sorted['decision'][len(df_sorted)-1],df_sorted['close'][len(df_sorted)-1]]
    pricel = df_sorted['open'][len(df_sorted)-1]
    decisionl = df_sorted['decision'][len(df_sorted)-1]
    return long, pricel, decisionl, data.index[z]

def get_closing():
    #This fails if closing is 
    from .models import Decision
    stocks = Decision.objects.filter(closingPrice=None)
    for stock in stocks:
        ticker = stock.stock.ticker
        tickDate = stock.tradeDate
        if timezone.now().date() > tickDate or timezone.now().time() > time(16,0,0):
            endDate = stock.tradeDate + timedelta(days=1)
            result = yf.Ticker(ticker).history(start=tickDate, end=endDate)
            closing = result["Close"].iloc[0]
            setattr(stock, "closingPrice", closing)
            stock.save()

def get_cashflows(ticker):
    stock = yf.Ticker(ticker)
    cf = stock.cashflow

    tCF = cf.filter(items=['Total Cash From Operating Activities', 'Total Cash From Financing Activities','Total Cashflows From Investing Activities'], axis=0)
    jsonVals = tCF.to_dict(orient="index")
    return jsonVals


def daily_email(user):
    from .models import Decision
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
