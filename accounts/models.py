from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from api.models import Stock, StockHolding
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email_address"), unique=True)
    # stocks = models.ManyToManyField(Stock, blank=True)
    stock_holding = models.ManyToManyField(StockHolding, blank=True)
    created = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=120, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
