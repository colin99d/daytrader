from .models import Stock, Algorithm, Decision
from django.contrib import admin


# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ["ticker","name","price","exchange","last_updated","active","listed"]
    search_fields = ["ticker",]

class AlgorithmAdmin(admin.ModelAdmin):
    pass

class DecisionHistroyAdmin(admin.ModelAdmin):
    list_display = ["stock", "algorithm", "open_price", "closing_price","confidence","trade_date"]

admin.site.register(Stock, StockAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Decision, DecisionHistroyAdmin)