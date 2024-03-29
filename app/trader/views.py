from .serializers import DecisionGetSerializer, DecisionSerializer, StockSerializer, AlgorithmSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Algorithm, Decision, Stock
from .functions.scrapers import valid_ticker
from rest_framework.response import Response
from rest_framework import viewsets, status
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
        if valid_ticker(ticker):
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

    def get_queryset(self):
        premium = self.request.user.premium
        if premium:
            return Algorithm.objects.all()
        else:
            return Algorithm.objects.filter(public=True)


@csrf_exempt
def cashflows(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        form.is_valid()
        content = form.cleaned_data['ticker'].upper()
        expiration = form.cleaned_data['expiration']
        if expiration:
            try:
                stock = Stock.objects.get(ticker=content)
                options = stock.get_options_chain(expiration)
                return JsonResponse({"options": options})
            except ObjectDoesNotExist:
                return HttpResponse(status=406)
        else:
            try:
                stock = Stock.objects.get(ticker=content)
                cashflows = stock.get_cashflows()
                info = stock.get_info()
                options = stock.get_options_chain()
                return JsonResponse({"cashflows": cashflows, "info": info, "options": options})
            except ObjectDoesNotExist:
                return HttpResponse(status=406)