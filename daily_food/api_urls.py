from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='auth')),
    path('diary/', include('apps.diary.urls', namespace='diary')),
    path('food/', include('apps.food.urls', namespace='food')),
]
