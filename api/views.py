from django.shortcuts import render

from .models import Stock
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, StockSerializer

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


class DashBoardViewSet(viewsets.ViewSet):
    pass
