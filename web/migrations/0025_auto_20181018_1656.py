# Generated by Django 2.1.1 on 2018-10-18 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0024_asset_category_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_property',
            name='manufacture',
            field=models.DateField(blank=True, null=True, verbose_name='出厂日期'),
        ),
        migrations.AlterField(
            model_name='asset_property',
            name='model',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='型号'),
        ),
        migrations.AlterField(
            model_name='asset_property',
            name='partlist',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='配件-多个'),
        ),
        migrations.AlterField(
            model_name='asset_property',
            name='purchase',
            field=models.DateField(blank=True, null=True, verbose_name='购买日期'),
        ),
        migrations.AlterField(
            model_name='asset_property',
            name='specifications',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='规格'),
        ),
        migrations.AlterField(
            model_name='asset_property',
            name='warranty',
            field=models.DateField(blank=True, null=True, verbose_name='维保到期'),
        ),
    ]
