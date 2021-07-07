from datetime import datetime
from bs4 import BeautifulSoup
import requests, re

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

def get_tickers(exchange):
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0']
    if exchange == "NASDAQ":
        base = 'https://www.advfn.com/nasdaq/nasdaq.asp?companies='
    elif exchange == "NYSE":
        base = 'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies='
    else:
        return None
    stocks = []
    
    for letter in letters:
        URL = base + letter
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        rows0 = soup.find_all('tr', attrs={'class':'ts0'})
        rows1 = soup.find_all('tr', attrs={'class':'ts1'})
        rows = rows0 + rows1
        for row in rows:
            cols = row.find_all('td')
            name = cols[0].text.strip()
            ticker = cols[1].text.strip()
            if  len(ticker) >= 1 and len(ticker) < 6:
                stocks.append({"name":name, "ticker":ticker,"exchange":exchange})
    return stocks 

def get_stock_info(stock):
    ticker = stock.ticker
    url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ ticker +'?modules=price'
    response = requests.get(url).json()["quoteSummary"]
    try:
        clean = response["result"][0]["price"]
        last_updated = datetime.fromtimestamp(clean["regularMarketTime"])
        openPrice = clean["regularMarketOpen"]["raw"]
        volume = clean["regularMarketVolume"]["raw"]
        setattr(stock,"last_updated",last_updated)
        setattr(stock,"price",openPrice)
        setattr(stock,"volume",volume)
        setattr(stock,"active",(volume > 0))
    except TypeError:
        if response['error']['code'] == 'Not Found':
            setattr(stock,"active",False)

    stock.save()
