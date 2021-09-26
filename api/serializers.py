from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Stock


class UserSerializer(serializers.HyperlinkedModelSerializer):

    stocks = serializers.SlugRelatedField(
        slug_field="short_code", read_only=True, many=True
    )

    class Meta:
        model = get_user_model()
        fields = ["url", "email", "full_name", "stocks"]


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ["url", "short_code", "price", "description"]
