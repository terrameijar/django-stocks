from django.db.models import query
from django.shortcuts import render

from .models import Stock, StockHolding
from rest_framework import viewsets, generics
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, StockSerializer, StockHoldingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = UserModel.objects.all().order_by("-created")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stocks to be viewed or edited.
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]


class DashBoardView(generics.ListAPIView):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]
    # queryset = UserModel.objects.all()
    # user_stocks = UserModel.stocks.all()

    def get_queryset(self):
        user = self.request.user
        print(user)
        # return user.stock_holding.filter(shares__gt=0)
        stock_holdings = StockHolding.objects.filter(user=user)
        print(stock_holdings)
        return stock_holdings
        # return user.stock_holding.all()


class AddUserStock(generics.CreateAPIView):
    queryset = StockHolding.objects.all()
    serializer_class = StockHoldingSerializer
