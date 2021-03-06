# Generated by Django 2.1.4 on 2019-01-03 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0021_auto_20181229_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='hr_attr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0, verbose_name='类型')),
                ('name', models.TextField(blank=True, max_length=64, null=True, verbose_name='名称')),
                ('value', models.TextField(blank=True, max_length=256, null=True, verbose_name='文本')),
                ('url', models.TextField(blank=True, max_length=256, null=True, verbose_name='网址')),
            ],
            options={
                'db_table': 'hr_attr',
            },
        ),
    ]
