# Generated by Django 3.1 on 2020-08-31 21:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EatingAction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время приема пищи')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='ощущения')),
            ],
            options={
                'verbose_name': 'прием пищи',
                'verbose_name_plural': 'приемы пищи',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('name', models.CharField(max_length=64, verbose_name='название')),
                ('mass', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='масса, г')),
                ('carbs', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='белки, г')),
                ('fats', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='жиры, г')),
                ('proteins', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='углеводы, г')),
                ('energy', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='энергия, кКал')),
                ('eating_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_items', to='food.eatingaction', verbose_name='прием пищи')),
            ],
            options={
                'verbose_name': 'продукт/блюдо',
                'verbose_name_plural': 'продукты/блюда',
            },
        ),
    ]
