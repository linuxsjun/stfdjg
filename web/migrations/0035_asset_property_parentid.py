# Generated by Django 2.1.1 on 2018-11-07 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0034_asset_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset_property',
            name='parentid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.asset_property'),
        ),
    ]