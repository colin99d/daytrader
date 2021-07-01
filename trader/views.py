from .serializers import DecisionGetSerializer, DecisionSerializer, StockSerializer, AlgorithmSerializer
from django.views.decorators.csrf import csrf_exempt
from .functions import valid_ticker, get_cashflows
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import JsonResponse
from .models import Algorithm, Decision, Stock
from django.shortcuts import render
from .forms import StockForm

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
        if valid_ticker(ticker) == True:
            response = serializer.data
            Stock.objects.create(ticker=ticker)
            sendStat = status.HTTP_201_CREATED 
        else:
            response = "Invalid ticker symbol"
            sendStat = status.HTTP_406_NOT_ACCEPTABLE

        return Response(response, status=sendStat)

class DecisionView(viewsets.ModelViewSet):
    queryset = Decision.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DecisionGetSerializer
        else:
            return DecisionSerializer

class AlgorithmView(viewsets.ModelViewSet):
    serializer_class = AlgorithmSerializer
    queryset = Algorithm.objects.all()



@csrf_exempt
def cashflows(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        form.is_valid()
        content = form.cleaned_data['ticker']
        cashflows = get_cashflows(content.upper())
        newCf = []
        for key in cashflows:
            newObj = {"id": key, "data": []}
            for key2, value in cashflows[key].items():
                date = key2.to_pydatetime().date().strftime("%m-%d-%Y")
                newObj["data"].append({"x":date, "y":value})
            newCf.append(newObj)
        return JsonResponse(newCf, safe=False)