# Generated by Django 4.1.4 on 2022-12-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_merge_20221214_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profile_picture',
            field=models.ImageField(blank=True, default='avatar.jpg', null=True, upload_to='images'),
        ),
    ]
