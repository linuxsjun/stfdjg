# Generated by Django 2.1 on 2018-09-04 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hr_hr',
            name='active',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]
