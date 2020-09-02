from rest_framework import generics

from . import models
from . import serializers


class WakingDayView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.WakingDaySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
