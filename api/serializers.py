from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Stock, StockHolding


class UserSerializer(serializers.HyperlinkedModelSerializer):

    stocks = serializers.SlugRelatedField(
        slug_field="short_code", read_only=True, many=True
    )

    class Meta:
        model = get_user_model()
        fields = ["url", "email", "full_name", "stocks"]


class StockHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockHolding
        fields = "__all__"
        optional_fields = [
            "notes",
            "shares",
            "avg_purchase_price",
            "dividends",
            "purchased_yield",
            "current_yield",
            "estimate_div_earnings",
        ]


class StockSerializer(serializers.HyperlinkedModelSerializer):
    short_code = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    dividend = serializers.SerializerMethodField()
    div_yield = serializers.SerializerMethodField()
    # shares = serializers.SerializerMethodField()

    # def get_shares(self, obj):
    #     return obj.stock.

    def get_div_yield(self, obj):
        return obj.stock.div_yield

    def get_dividend(self, obj):
        return obj.stock.dividend

    def get_description(self, obj):
        return obj.stock.description

    def get_short_code(self, obj):
        try:
            short_name = obj.stock.short_code
        except AttributeError as e:
            print(e)
            return ""

        return short_name

    def get_price(self, obj):
        return obj.stock.price

    class Meta:
        model = Stock
        fields = [
            "url",
            "short_code",
            "price",
            "description",
            "dividend",
            "div_yield",
            "shares",
        ]
