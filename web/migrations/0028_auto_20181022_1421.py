# Generated by Django 2.1.1 on 2018-10-22 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_auto_20181019_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_property',
            name='sid',
            field=models.CharField(max_length=24, unique=True, verbose_name='编号'),
        ),
    ]
