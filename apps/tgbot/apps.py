from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TgbotConfig(AppConfig):
    name = 'apps.tgbot'
    verbose_name = _('Бот для telegram')
