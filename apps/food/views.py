from rest_framework import generics, permissions

from . import models
from . import serializers


class FoodItemView(generics.ListCreateAPIView):
    queryset = models.FoodItem.objects.all()
    serializer_class = serializers.FoodItemSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly,
