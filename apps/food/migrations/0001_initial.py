# Generated by Django 3.1 on 2020-09-01 23:31

import apps.food.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EatingAction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('time_moment', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время приема пищи')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='ощущения')),
            ],
            options={
                'verbose_name': 'прием пищи',
                'verbose_name_plural': 'приемы пищи',
                'ordering': ('-time_moment',),
            },
        ),
        migrations.CreateModel(
            name='WakingDay',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('day', models.DateField(default=apps.food.models.now_day_with_tz, verbose_name='день')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='ощущения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eating_actions', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'день бодрствования',
                'verbose_name_plural': 'дни бодрствования',
                'ordering': ('-day',),
            },
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('name', models.CharField(max_length=64, verbose_name='название')),
                ('mass', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='масса, г')),
                ('carbs', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='белки, г')),
                ('fats', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='жиры, г')),
                ('proteins', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='углеводы, г')),
                ('energy', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='энергия, кКал')),
                ('eating_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_items', to='food.eatingaction', verbose_name='прием пищи')),
            ],
            options={
                'verbose_name': 'продукт/блюдо',
                'verbose_name_plural': 'продукты/блюда',
            },
        ),
        migrations.AddField(
            model_name='eatingaction',
            name='waking_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eating_actions', to='food.wakingday', verbose_name='день бодрствования'),
        ),
    ]
