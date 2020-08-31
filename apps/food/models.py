import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.db import connection
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EatingAction(models.Model):
    class Meta:
        verbose_name = _('прием пищи')
        verbose_name_plural = _('приемы пищи')
        ordering = '-time_moment',

    id = models.UUIDField(
        verbose_name=_('идентификатор'), primary_key=True,
        editable=False, default=uuid.uuid4
    )
    time_moment = models.DateTimeField(
        verbose_name=_('время приема пищи'), default=timezone.now
    )
    comment = models.TextField(
        verbose_name=_('ощущения'), null=True, blank=True
    )

    @classmethod
    def get_by_date(cls):
        fields = 'mass', 'carbs', 'fats', 'proteins', 'energy',

        annotations = ','.join(f'SUM("food_fooditem"."{field}") AS "{field}"'
                               for field in fields)

        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT DATE_TRUNC('day',  "food_eatingaction"."time_moment"
            AT TIME ZONE 'Europe/Moscow') AS "day", {annotations}
            FROM "food_eatingaction" LEFT OUTER JOIN "food_fooditem"
            ON ("food_eatingaction"."id" = "food_fooditem"."eating_action_id")
            GROUP BY DATE_TRUNC('day', "food_eatingaction"."time_moment"
            AT TIME ZONE 'Europe/Moscow') ORDER BY "day";
            ''')

            return list(map(
                lambda x: (x[0], {f: x[i + 1] for i, f in enumerate(fields)}),
                cursor.fetchall()
            ))



    def __str__(self) -> str:
        return self.time_moment.strftime('%Y-%m-%d %H:%M:%S')


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
    mass = models.DecimalField(
        verbose_name=_('масса, г'), null=True, blank=True,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    carbs = models.DecimalField(
        verbose_name=_('белки, г'), null=True, blank=True,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    fats = models.DecimalField(
        verbose_name=_('жиры, г'), null=True, blank=True,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    proteins = models.DecimalField(
        verbose_name=_('углеводы, г'), null=True, blank=True,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    energy = models.DecimalField(
        verbose_name=_('энергия, кКал'), null=True, blank=True,
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return self.name
