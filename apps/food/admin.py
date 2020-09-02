from django.contrib import admin
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from . import models
from . import forms


class FoodItemInline(admin.StackedInline):
    model = models.FoodItem
    extra = 0


def build_admin_field(name: str, description: str) -> callable:
    def func(obj):
        return getattr(obj, name) or 0
    func.__name__ = name
    func.short_description = description
    func.admin_order_field = name
    return func


class AnnotatedMixin:
    annotated_fields = {
        'mass': _('общая масса, г'),
        'carbs': _('сумма белков, г'),
        'fats': _('сумма жиров, г'),
        'proteins': _('сумма углеводов, г'),
        'energy': _('общая энергия, кКал'),
    }

    list_display = tuple(annotated_fields.keys())
    readonly_fields = tuple(annotated_fields.keys())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, description in self.annotated_fields.items():
            setattr(self, name, build_admin_field(name, description))


@admin.register(models.EatingAction)
class EatingActionAdmin(AnnotatedMixin, admin.ModelAdmin):
    list_display = 'time_moment', *AnnotatedMixin.list_display, 'comment',
    inlines = FoodItemInline,

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not request.user.is_superuser:
            return forms.EatingActionCreateForm
        return super().get_form(request, obj, change, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        annotates = {
            name: Sum(f'food_items__{name}') for name in self.annotated_fields
        }
        return qs.annotate(**annotates)


class EatingActionInline(admin.StackedInline):
    model = models.EatingAction
    extra = 0


@admin.register(models.WakingDay)
class WakingDayAdmin(AnnotatedMixin, admin.ModelAdmin):
    list_display = 'day', *AnnotatedMixin.list_display, 'comment',
    inlines = EatingActionInline,

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        annotates = {
            name: Sum(f'eating_actions__food_items__{name}')
            for name in self.annotated_fields
        }
        return qs.annotate(**annotates)
