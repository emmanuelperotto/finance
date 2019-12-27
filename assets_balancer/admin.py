from django.contrib import admin
from .models import Sector, Asset, Order

class AssetView(admin.ModelAdmin):
    list_display = ("id", "ticket", "price_cap", "rating", "category", "sector")
    list_editable = ("price_cap", "rating")
    list_filter = ("category", "sector")

admin.site.register(Sector)
admin.site.register(Asset, AssetView)
admin.site.register(Order)
