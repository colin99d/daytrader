from bs4 import BeautifulSoup
import requests, re


def valid_ticker(symbol):
    url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ symbol.upper() +'?modules=price'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' }
    response = requests.get(url, headers=headers).content.decode('utf-8')
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

def get_highest_performing():
    URL = 'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class':'tv-data-table'})
    body = table.find('tbody')
    rows = body.find_all('tr')
    cols = rows[0].find_all('td')
    item = cols[0].find('a').text.strip()
    return item

def get_highest_performing():
    URL = 'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class':'tv-data-table'})
    body = table.find('tbody')
    rows = body.find_all('tr')
    cols = rows[0].find_all('td')
    item = cols[0].find('a').text.strip()
    return item

def get_lowest_performing():
    URL = 'https://www.tradingview.com/markets/stocks-usa/market-movers-losers/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class':'tv-data-table'})
    body = table.find('tbody')
    rows = body.find_all('tr')
    cols = rows[0].find_all('td')
    item = cols[0].find('a').text.strip()
    return item