# Generated by Django 3.2.5 on 2021-07-26 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user')], default='user', max_length=20, verbose_name='Уровень доступа'),
        ),
    ]
