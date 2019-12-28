from django.contrib import admin
from .models import Sector, Asset, Order

class AssetView(admin.ModelAdmin):
    list_display = ("id", "ticket", "current_price", "current_price_updated_at",
                    "price_cap", "rating", "category", "sector")
    list_editable = ("current_price", "price_cap", "rating")
    list_filter = ("category", "sector")
    list_display_links = ("id", "ticket")

admin.site.register(Sector)
admin.site.register(Asset, AssetView)
admin.site.register(Order)
