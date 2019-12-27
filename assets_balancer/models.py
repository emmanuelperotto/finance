from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator

class Sector(models.Model):
    # Fields
    name = models.CharField(max_length=200, unique=True)

    # Methods
    def __str__(self):
        return self.name

class Asset(models.Model):
    # Relationships
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    # Enums
    class Kind(models.IntegerChoices):
        STOCK = 0
        FII = 1
        REIT = 2
        ETF = 3
        CRYPTO = 4

    # Fields
    category = models.IntegerField(choices=Kind.choices)
    ticket = models.CharField(max_length=200, unique=True)
    rating = models.IntegerField()
    price_cap = MoneyField(decimal_places=2,
                           max_digits=14,
                           null=True,
                           default_currency="BRL",
                           validators=[MinMoneyValidator({'BRL': 0})])

    # Methods
    def __str__(self):
        return self.ticket

class Order(models.Model):
    # Relationships
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    # Fields
    quantity = models.IntegerField()
    price = MoneyField(decimal_places=2,
                       max_digits=14,
                       default_currency="BRL",
                       validators=[MinMoneyValidator({'BRL': 0})])
    created_at = models.DateTimeField(default=timezone.now)

    # Methods

    def __str__(self):
        return f"{self.asset.ticket} - {self.quantity} x {self.price}"
