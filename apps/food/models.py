import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class FoodItem(models.Model):
    class Meta:
        verbose_name = _('продукт/блюдо')
        verbose_name_plural = _('продукты/блюда')

    id = models.UUIDField(
        verbose_name=_('идентификатор'), primary_key=True,
        editable=False, default=uuid.uuid4
    )
    name = models.CharField(verbose_name=_('название'), max_length=64)
    carbs = models.DecimalField(
        verbose_name=_('белки, г'), default=0,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    fats = models.DecimalField(
        verbose_name=_('жиры, г'), default=0,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    proteins = models.DecimalField(
        verbose_name=_('углеводы, г'), default=0,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    calories = models.DecimalField(
        verbose_name=_('калории, кКал'), default=0,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return self.name
