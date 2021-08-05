# Generated by Django 3.2.5 on 2021-08-05 09:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Быстрее не получится')], verbose_name='Время приготовления (в минутах)'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Не надо жадничать')], verbose_name='Количество в рецепте'),
        ),
    ]