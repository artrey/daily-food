import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EatingAction(models.Model):
    class Meta:
        verbose_name = _('прием пищи')
        verbose_name_plural = _('приемы пищи')
        ordering = '-date',

    id = models.UUIDField(
        verbose_name=_('идентификатор'), primary_key=True,
        editable=False, default=uuid.uuid4
    )
    date = models.DateTimeField(
        verbose_name=_('время приема пищи'), default=timezone.now
    )
    comment = models.TextField(
        verbose_name=_('ощущения'), null=True, blank=True
    )

    def __str__(self) -> str:
        return self.date.strftime('%Y-%m-%d %H:%M:%S')


class FoodItem(models.Model):
    class Meta:
        verbose_name = _('продукт/блюдо')
        verbose_name_plural = _('продукты/блюда')

    id = models.UUIDField(
        verbose_name=_('идентификатор'), primary_key=True,
        editable=False, default=uuid.uuid4
    )
    eating_action = models.ForeignKey(
        EatingAction, on_delete=models.CASCADE,
        verbose_name=_('прием пищи'), related_name='food_items'
    )
    name = models.CharField(verbose_name=_('название'), max_length=64)
    mass = models.FloatField(
        verbose_name=_('масса, г'), null=True, blank=True,
        validators=[MinValueValidator(0)],
    )
    carbs = models.FloatField(
        verbose_name=_('белки, г'), null=True, blank=True,
        validators=[MinValueValidator(0)],
    )
    fats = models.FloatField(
        verbose_name=_('жиры, г'), null=True, blank=True,
        validators=[MinValueValidator(0)],
    )
    proteins = models.FloatField(
        verbose_name=_('углеводы, г'), null=True, blank=True,
        validators=[MinValueValidator(0)],
    )
    energy = models.FloatField(
        verbose_name=_('энергия, кКал'), null=True, blank=True,
        validators=[MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return self.name
