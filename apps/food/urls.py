from django.urls import path

from . import views


urlpatterns = [
    path('', views.add_view, name='add'),
    path('charts/', views.charts_view, name='charts'),
]
