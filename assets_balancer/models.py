from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money
from django.dispatch import receiver
from django.db.models.signals import pre_save

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
    current_price = MoneyField(decimal_places=2,
                               max_digits=14,
                               null=True,
                               blank=True,
                               default_currency="BRL",
                               validators=[MinMoneyValidator({'BRL': 0})])
    current_price_updated_at = models.DateTimeField(null=True, blank=True)

    # Methods
    def __str__(self):
        return self.ticket

    def total_quantity(self):
        result = self.order_set.all().aggregate(models.Sum("quantity"))
        quantity = result.get("quantity__sum") or 0

        return quantity

    def ideal_percentage(self):
        percentage = (self.rating / Asset.rating_sum()) * 100
        return round(percentage, 2)

    def current_percentage(self):
        if Order.total_equity() <= Money(0, "BRL"):
            return 0

        percentage = (self.value_invested() / Order.total_equity()) * 100
        return round(percentage, 2)

    def average_price(self):
        if self.total_quantity() == 0:
            return 0

        return self.value_invested() / self.total_quantity()

    def value_invested(self):
        orders = self.order_set.all()
        value = sum(list(map(lambda order: order.total_price(), orders)))

        if value == 0:
            return Money(0, "BRL")

        return value

    def market_value(self):
        if self.total_quantity() and self.current_price:
            return self.total_quantity() * self.current_price

        return Money(0, "BRL")

    def variation(self):
        if self.value_invested() == Money(0, "BRL"):
            return 0

        percentage = ((self.market_value() - self.value_invested()) / self.value_invested()) * 100

        return round(percentage, 2)

    def status(self):
        if self.current_percentage() <= self.ideal_percentage():
            return "Buy"

        return "Hold"

    def can_update_current_price(self):
        if not self.current_price_updated_at:
            return True

        time_diff = timezone.now() - self.current_price_updated_at
        return (time_diff.seconds / 60.0) > 60

    @staticmethod
    def rating_sum():
        result = Asset.objects.aggregate(models.Sum("rating"))
        value = result.get("rating__sum") or 0

        return value

class Order(models.Model):
    # Relationships
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    # Fields
    quantity = models.IntegerField()
    unit_price = MoneyField(decimal_places=2,
                            max_digits=14,
                            default_currency="BRL",
                            validators=[MinMoneyValidator({'BRL': 0})])
    created_at = models.DateTimeField(default=timezone.now)

    # Methods

    def __str__(self):
        return f"{self.asset.ticket} - {self.quantity} x {self.unit_price}"

    def total_price(self):
        if self.unit_price and self.quantity:
            return self.unit_price * self.quantity

        return Money(0, "BRL")

    @staticmethod
    def total_equity():
        orders = Order.objects.all()
        value = sum(list(map(lambda order: order.total_price(), orders)))

        if value == 0:
            return Money(0, "BRL")

        return value


@receiver(pre_save, sender=Asset)
def change_current_price_updated_at(sender, instance, **kwargs):
    try:
        asset = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # Object is new, so field hasn't technically changed
    else:
        if not asset.current_price == instance.current_price: # Field has changed
            setattr(instance, "current_price_updated_at", timezone.now())
