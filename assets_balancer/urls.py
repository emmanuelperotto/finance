from django.urls import path
from .views import assets, update_current_price

urlpatterns = [
    path("", assets, name='assets'),
    path("update_current_price", update_current_price, name='update_current_price')
]
