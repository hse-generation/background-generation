# Generated by Django 4.1.4 on 2023-05-17 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_alter_users_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_onboarding_passed',
            field=models.IntegerField(default=0, verbose_name='Онбординг пройден?'),
        ),
    ]