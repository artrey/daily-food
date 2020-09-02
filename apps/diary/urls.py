from django.urls import path

from . import views


app_name = 'diary'

urlpatterns = [
    path('waking_day/<pk>/', views.WakingDayView.as_view(), name='waking_day'),
]
