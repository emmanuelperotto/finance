import requests
from django.utils import timezone
from .models import Asset

class UpdateAssetCurrentPrice():
    API_URL = "https://www.alphavantage.co/query"

    def __init__(self, ticket):
        self.ticket = ticket
        self.asset = Asset.objects.get(ticket=ticket)
        self.errors = {}

    def call(self):
        query_params = {
            "function": "GLOBAL_QUOTE",
            "symbol": f"{self.ticket}.SAO",
            "apikey": "FT8J6BP77CEQKVRU"
        }

        response = requests.get(self.API_URL, params=query_params)

        if response.status_code == requests.codes["ok"]:
            response_body = response.json()
            price = float(response_body.get("Global Quote").get("05. price"))
            self.asset.current_price = price
            self.asset.current_price_updated_at = timezone.now()
            self.asset.save()

            return price

        self.errors = response.json()
        return None
