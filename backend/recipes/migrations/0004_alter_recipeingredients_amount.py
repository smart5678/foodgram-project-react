# Generated by Django 3.2.5 on 2021-07-29 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipeingredients_recipe-ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='Количество в рецепте'),
        ),
    ]