# Generated by Django 3.1.1 on 2020-09-02 20:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EatingFood',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('mass', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='масса, г')),
                ('eating_action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eating_foods', to='diary.eatingaction', verbose_name='прием пищи')),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eating_foods', to='food.fooditem', verbose_name='продукт/блюдо')),
            ],
            options={
                'verbose_name': 'съеденная пища',
                'verbose_name_plural': 'съеденная пища',
                'unique_together': {('eating_action', 'food_item')},
            },
        ),
        migrations.DeleteModel(
            name='FoodItem',
        ),
        migrations.AddField(
            model_name='eatingaction',
            name='food_items',
            field=models.ManyToManyField(related_name='eating_actions', through='diary.EatingFood', to='food.FoodItem', verbose_name='продукты/блюда'),
        ),
    ]
