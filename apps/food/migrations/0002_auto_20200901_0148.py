# Generated by Django 3.1 on 2020-08-31 22:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='carbs',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='белки, г'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='energy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='энергия, кКал'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='fats',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='жиры, г'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='mass',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='масса, г'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='proteins',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='углеводы, г'),
        ),
    ]