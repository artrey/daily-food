from django.urls import path

from . import views


urlpatterns = [
    path('', views.charts_view, name='charts'),
]
