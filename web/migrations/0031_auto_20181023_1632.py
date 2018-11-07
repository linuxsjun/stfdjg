# Generated by Django 2.1.1 on 2018-10-23 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0030_asset_category_autosid'),
    ]

    operations = [
        migrations.AddField(
            model_name='hr_department',
            name='type',
            field=models.IntegerField(default=0, verbose_name='组织类型:行政/项目'),
        ),
        migrations.AlterField(
            model_name='hr_department',
            name='order',
            field=models.IntegerField(null=True, verbose_name='部门主管'),
        ),
    ]