from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from .models import Asset, Order
from .commands import UpdateAssetCurrentPrice

# Create your views here.
def assets(request):
    assets_list = Asset.objects.all()
    total_market_value = sum(list(map(lambda asset: asset.market_value(), assets_list)))
    context = {
        "assets": assets_list,
        "total_equity": Order.total_equity(),
        "total_market_value": total_market_value
    }


    return render(request, "assets_balancer/assets.html", context)

def update_current_price(request):
    try:
        ticket = request.POST.get("ticket")
        command = UpdateAssetCurrentPrice(ticket)
        price = command.call()

        if price:
            return JsonResponse({"price": price})

        return JsonResponse({"errors": command.errors}, status=422)
    except Exception as exception:
        return JsonResponse({"error": exception}, status=422)
