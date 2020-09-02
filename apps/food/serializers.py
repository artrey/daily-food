from rest_framework import serializers

from . import models


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FoodItem
        fields = '__all__'
