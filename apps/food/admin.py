from django.contrib import admin
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from . import models


class FoodItemInline(admin.StackedInline):
    model = models.FoodItem
    extra = 0


def build_admin_field(name: str, description: str) -> callable:
    def func(obj):
        return getattr(obj, name) or 0
    func.__name__ = name
    func.short_description = description
    return func


@admin.register(models.EatingAction)
class EatingActionAdmin(admin.ModelAdmin):
    annotated_fields = {
        'mass': _('общая масса, г'),
        'carbs': _('сумма белков, г'),
        'fats': _('сумма жиров, г'),
        'proteins': _('сумма углеводов, г'),
        'energy': _('общая энергия, кКал'),
    }

    list_display = 'time_moment', *tuple(annotated_fields.keys()), 'comment',
    list_filter = 'time_moment',
    readonly_fields = tuple(annotated_fields.keys())
    inlines = FoodItemInline,

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, description in self.annotated_fields.items():
            setattr(self, name, build_admin_field(name, description))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        annotates = {
            name: Sum(f'food_items__{name}') for name in self.annotated_fields
        }
        return qs.annotate(**annotates)
