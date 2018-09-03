# Generated by Django 2.0.6 on 2018-09-01 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='base_menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='菜单')),
                ('nameid', models.CharField(max_length=8, unique=True, verbose_name='菜单编号')),
                ('status', models.FloatField(default=True)),
                ('parentid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.base_menu', to_field='nameid', verbose_name='上级菜单')),
            ],
            options={
                'db_table': 'base_menu',
            },
        ),
    ]
