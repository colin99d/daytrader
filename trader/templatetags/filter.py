from django import template

register = template.Library()

def growth(value, arg):
    decimal = (value - arg) / arg
    percent = decimal * 100
    return str(round(percent,2)) + "%"

register.filter('growth', growth)