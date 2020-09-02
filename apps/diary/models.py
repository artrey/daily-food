import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.food.models import FoodItem


User = get_user_model()


class UserDiaryParams(models.Model):
    class Meta:
        verbose_name = _('настройки пользователя')
        verbose_name_plural = _('настройки пользователей')

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='diary_params',
        primary_key=True, verbose_name=_('пользователь'),
    )
    normal_daily_energy = models.DecimalField(
        verbose_name=_('суточная норма, кКал'), null=True, blank=True,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return str(self.user)


@receiver(post_save, sender=User, dispatch_uid='create_user_diary_params')
def create_user_diary_params(instance: User, created: bool, **kwargs):
    if not created:
        return

    UserDiaryParams.objects.create(user=instance)


def now_day_with_tz():
    return timezone.make_naive(timezone.now()).date()


class WakingDay(models.Model):
    class Meta:
        verbose_name = _('день бодрствования')
        verbose_name_plural = _('дни бодрствования')
        ordering = '-day',

    id = models.UUIDField(
        verbose_name=_('идентификатор'), primary_key=True,
        editable=False, default=uuid.uuid4
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name=_('пользователь'), related_name='eating_actions'
    )
    day = models.DateField(
        verbose_name=_('день'), default=now_day_with_tz
    )
    comment = models.TextField(
        verbose_name=_('ощущения'), null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.day)


class EatingAction(models.Model):
    class Meta:
        verbose_name = _('прием пищи')
        verbose_name_plural = _('приемы пищи')
        ordering = '-time_moment',

    id = models.UUIDField(
        verbose_name=_('идентификатор'), primary_key=True,
        editable=False, default=uuid.uuid4
    )
    waking_day = models.ForeignKey(
        WakingDay, on_delete=models.CASCADE,
        verbose_name=_('день бодрствования'), related_name='eating_actions'
    )
    time_moment = models.DateTimeField(
        verbose_name=_('время приема пищи'), default=timezone.now
    )
    food_items = models.ManyToManyField(
        FoodItem, through='EatingFood', related_name='eating_actions',
        verbose_name=_('продукты/блюда')
    )
    comment = models.TextField(
        verbose_name=_('ощущения'), null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.time_moment)


class EatingFood(models.Model):
    class Meta:
        verbose_name = _('съеденная пища')
        verbose_name_plural = _('съеденная пища')
        unique_together = 'eating_action', 'food_item',

    id = models.UUIDField(
        verbose_name=_('идентификатор'), primary_key=True,
        editable=False, default=uuid.uuid4
    )
    eating_action = models.ForeignKey(
        EatingAction, on_delete=models.CASCADE,
        verbose_name=_('прием пищи'), related_name='eating_foods',
    )
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE,
        verbose_name=_('продукт/блюдо'), related_name='eating_foods',
    )
    mass = models.DecimalField(
        verbose_name=_('масса, г'), default=0,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return f'{self.food_item.name} | {self.mass}'
