from django.contrib import admin

from . import models


@admin.register(models.FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = 'name', 'carbs', 'fats', 'proteins', 'calories',
    search_fields = 'name',
