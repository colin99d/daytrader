from django.shortcuts import render
from .functions import valid_ticker, daily_email
from .forms import StockForm
from .models import DecisionHistory, Stock

# Create your views here.
def home(request):
    if request.method == "GET":
        form = StockForm()
        error = None
        
    elif request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker'].upper()
            if ticker == "" or ticker is None:
                error =  "Invalid Ticker Symbol"
            elif ticker.upper() in [x.ticker.upper() for x in Stock.objects.all()]:
                error = "The stock is already being monitored"
            elif valid_ticker(ticker) == True:
                Stock.objects.create(ticker=ticker)
                error = None
            else:
                error = "Invalid ticker symbol"
        else:
            error = "Invalid form"

    context = {"stocks": Stock.objects.all(), "form": form}
    if error:
        context["error"] = error

    daily_email(request)
    return render(request, 'home.html', context)

def table(request):
    if request.method == "GET":
        pass
    context = {"stocks": DecisionHistory.objects.all()}

    return render(request, 'table.html', context)
