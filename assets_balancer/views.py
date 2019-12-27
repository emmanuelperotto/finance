from django.shortcuts import render
from .models import Asset

# Create your views here.
def assets(request):
    assets_list = Asset.objects.all()

    return render(request, "assets_balancer/assets.html", {"assets": assets_list})
