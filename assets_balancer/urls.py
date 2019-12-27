from django.urls import path
from .views import assets

urlpatterns = [
    path("", assets, name='assets')
]