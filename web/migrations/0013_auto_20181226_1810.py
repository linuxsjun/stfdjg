# Generated by Django 2.1.4 on 2018-12-26 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20181226_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_application',
            name='appltno',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='申请单编号'),
        ),
    ]