# Generated by Django 2.1.4 on 2018-12-27 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20181226_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='base_flowlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formtplid', models.CharField(max_length=16, null=True, verbose_name='模板编号号')),
                ('type', models.IntegerField(default=0, verbose_name='流程类型')),
                ('sequence', models.IntegerField(default=1, verbose_name='顺序')),
                ('personnel', models.IntegerField(default=0, verbose_name='签署对象')),
                ('pertype', models.IntegerField(default=0, verbose_name='对象类型')),
                ('signtype', models.IntegerField(default=0, verbose_name='签署方式')),
                ('logical', models.CharField(blank=True, max_length=128, null=True, verbose_name='流程逻辑')),
            ],
            options={
                'db_table': 'base_flowlist',
            },
        ),
    ]
