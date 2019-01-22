# Generated by Django 2.1.4 on 2019-01-10 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0026_base_flowlist_tpl'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset_category',
            name='displayname',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='显示'),
        ),
        migrations.AlterField(
            model_name='asset_category',
            name='parentid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.asset_category', verbose_name='上一级'),
        ),
    ]