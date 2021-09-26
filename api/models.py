from django.db import models
from django.contrib.auth import get_user_model


class Stock(models.Model):
    name = models.CharField(max_length=120)
    price = models.FloatField()
    short_code = models.CharField(max_length=12)
    description = models.TextField()
    dividend = models.FloatField(blank=True, null=True)
    div_yield = models.FloatField(blank=True, null=True)
    div_cagr = models.FloatField(blank=True, null=True)
    sector = models.CharField(max_length=120, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    next_ex_div_date = models.DateField(blank=True, null=True)
    next_pay_date = models.DateField(blank=True, null=True)
    market_cap = models.FloatField(blank=True, null=True)
    payout_ratio = models.FloatField(blank=True, null=True)
    shares = models.FloatField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now_add=True)
    avg_purchase_price = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


# class Profile(models.Model):
#     user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=120, blank=True, null=True)
#     created = models.DateTimeField(auto_now=True)

#     stocks = models.ManyToManyField(Stock)

#     def __str__(self) -> str:
#         return f"{self.user.username} Profile"
