# Generated by Django 2.1.1 on 2018-09-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20180904_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_category',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='名称'),
        ),
    ]