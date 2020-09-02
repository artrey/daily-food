from rest_framework import serializers

from . import models


class WakingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WakingDay
        fields = '__all__'
