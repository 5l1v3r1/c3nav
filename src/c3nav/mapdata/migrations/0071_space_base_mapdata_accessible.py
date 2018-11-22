# Generated by Django 2.1.1 on 2018-11-20 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0070_auto_20180918_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='base_mapdata_accessible',
            field=models.BooleanField(default=False, verbose_name='always accessible (overwrites base mapdata setting)'),
        ),
    ]