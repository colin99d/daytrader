from .serializers import DecisionSerializer, StockSerializer
from .functions import valid_ticker, get_cashflows
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import JsonResponse
from .models import Decision, Stock
from django.shortcuts import render
import json

# Create your views here.
def home(request):
    if request.method == "GET":
        return render(request, 'home.html')

class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticker = serializer.validated_data.get('ticker').upper()
        if ticker == "" or ticker is None:
            response =  "Invalid Ticker Symbol"
            sendStat = status.HTTP_406_NOT_ACCEPTABLE
        elif ticker.upper() in [x.ticker.upper() for x in Stock.objects.all()]:
            response = "The stock is already being monitored"
            sendStat = status.HTTP_406_NOT_ACCEPTABLE
        elif valid_ticker(ticker) == True:
            response = serializer.data
            Stock.objects.create(ticker=ticker)
            sendStat = status.HTTP_201_CREATED 
        else:
            response = "Invalid ticker symbol"
            sendStat = status.HTTP_406_NOT_ACCEPTABLE

        return Response(response, status=sendStat)

class DecisionView(viewsets.ModelViewSet):
    serializer_class = DecisionSerializer
    queryset = Decision.objects.all()

@csrf_exempt
def cashflows(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['ticker']
        cashflows = get_cashflows(content.upper())
        newCf = []
        for key in cashflows:
            newObj = {"id": key, "data": []}
            for key2, value in cashflows[key].items():
                date = key2.to_pydatetime().date().strftime("%m-%d-%Y")
                newObj["data"].append({"x":date, "y":value})
            newCf.append(newObj)
        return JsonResponse(newCf, safe=False)