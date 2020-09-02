from django.urls import path

from . import views


app_name = 'food'

urlpatterns = [
    path('', views.FoodItemView.as_view(), name='food-list'),
]
