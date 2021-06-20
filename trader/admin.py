from .models import Stock, Algorithm, Decision
from django.contrib import admin


# Register your models here.
class StockAdmin(admin.ModelAdmin):
    pass

class AlgorithmAdmin(admin.ModelAdmin):
    pass

class DecisionHistroyAdmin(admin.ModelAdmin):
    list_display = ["stock", "algorithm", "openPrice", "closingPrice","confidence","tradeDate"]

admin.site.register(Stock, StockAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Decision, DecisionHistroyAdmin)