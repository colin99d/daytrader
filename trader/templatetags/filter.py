from django import template

register = template.Library()

def growth(open, close):
    decimal = (close - open) / open
    percent = decimal * 100
    return str(round(percent,2)) + "%"

register.filter('growth', growth)