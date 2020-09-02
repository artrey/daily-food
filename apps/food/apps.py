from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FoodConfig(AppConfig):
    name = 'apps.food'
    verbose_name = _('Продукты и блюда')
