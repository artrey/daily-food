import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
    comment = models.TextField(
        verbose_name=_('ощущения'), null=True, blank=True
    )

    @classmethod
    def get_by_date(cls, user, date: timezone = None):
        fields = 'mass', 'carbs', 'fats', 'proteins', 'energy',

        annotations = ','.join(f'SUM("food_fooditem"."{field}") AS "{field}"'
                               for field in fields)

        having_constraints = []
        if date:
            having_constraints.append('''
            DATE_TRUNC('day', "food_eatingaction"."time_moment"
            AT TIME ZONE 'Europe/Moscow') = DATE_TRUNC('day', %s
            AT TIME ZONE 'Europe/Moscow')
            ''')
        having_string = ''
        if having_constraints:
            having_string = 'HAVING ' + ' AND '.join(having_constraints)

        with connection.cursor() as cursor:
            cursor.execute(f'''
            SELECT DATE_TRUNC('day', "food_eatingaction"."time_moment"
            AT TIME ZONE 'Europe/Moscow') AS "day", {annotations}
            FROM "food_eatingaction" LEFT OUTER JOIN "food_fooditem"
            ON ("food_eatingaction"."id" = "food_fooditem"."eating_action_id")
            WHERE "food_eatingaction"."user_id" = %s
            GROUP BY DATE_TRUNC('day', "food_eatingaction"."time_moment"
            AT TIME ZONE 'Europe/Moscow')
            {having_string}
            ORDER BY "day";
            ''', (user.id, date,) if date else (user.id,))

            return list(map(
                lambda x: (x[0], {f: x[i + 1] for i, f in enumerate(fields)}),
                cursor.fetchall()
            ))

    def __str__(self) -> str:
        return str(self.time_moment)


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
