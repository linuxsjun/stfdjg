# Generated by Django 2.1 on 2018-09-04 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20180904_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_category',
            name='parentid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.asset_category'),
        ),
    ]