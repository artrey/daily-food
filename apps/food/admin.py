from django.contrib import admin
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from . import models


class FoodItemInline(admin.StackedInline):
    model = models.FoodItem
    extra = 0


@admin.register(models.EatingAction)
class EatingActionAdmin(admin.ModelAdmin):
    list_display = 'date', 'mass', 'energy', 'comment',
    list_filter = 'date',
    readonly_fields = 'mass', 'energy',
    inlines = FoodItemInline,

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('food_items').annotate(
            mass=Sum('food_items__mass'), energy=Sum('food_items__energy')
        )

    def mass(self, obj: models.EatingAction) -> int:
        return getattr(obj, 'mass') or 0
    mass.short_description = _('общая масса, г')

    def energy(self, obj: models.EatingAction) -> int:
        return getattr(obj, 'energy') or 0
    energy.short_description = _('общая энергия, кКал')
