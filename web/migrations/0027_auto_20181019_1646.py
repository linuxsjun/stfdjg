# Generated by Django 2.1.1 on 2018-10-19 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0026_asset_property_bom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_parts',
            name='bom',
            field=models.BooleanField(default=True, verbose_name='组件'),
        ),
    ]
