from django import template

register = template.Library()

def growth(open, close):
    try:
        decimal = (close - open) / open
        percent = str(round(decimal * 100,2)) + "%"
    except TypeError:
        percent = "N/A"
    except ZeroDivisionError:
        percent = "N/A"
    return percent

register.filter('growth', growth)