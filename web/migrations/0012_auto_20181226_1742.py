# Generated by Django 2.1.4 on 2018-12-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_asset_application_backdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_application',
            name='appdate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='申请时间'),
        ),
    ]
