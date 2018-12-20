# Generated by Django 2.1.1 on 2018-12-11 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_asset_allot'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset_allot',
            name='active',
            field=models.BooleanField(default=True, verbose_name='有效的'),
        ),
        migrations.AddField(
            model_name='asset_allot',
            name='assetid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.asset_property', verbose_name='分配设备'),
        ),
        migrations.AddField(
            model_name='asset_allot',
            name='goreturn',
            field=models.DateField(blank=True, null=True, verbose_name='归还时间'),
        ),
        migrations.AddField(
            model_name='asset_allot',
            name='perreturn',
            field=models.DateField(blank=True, null=True, verbose_name='预归还时间'),
        ),
        migrations.AddField(
            model_name='asset_allot',
            name='type',
            field=models.IntegerField(blank=True, null=True, verbose_name='借用/领用'),
        ),
        migrations.AlterModelTable(
            name='asset_allot',
            table='asset_allot',
        ),
    ]