from django import forms

class StockForm(forms.Form):
    ticker = forms.CharField(max_length=5)
    expiration = forms.IntegerField(required=False)