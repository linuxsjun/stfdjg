# Generated by Django 2.1.4 on 2018-12-28 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_auto_20181228_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset_allot',
            name='managerin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managerin', to='web.hr_hr', verbose_name='回收人'),
        ),
        migrations.AddField(
            model_name='asset_allot',
            name='managerout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managerout', to='web.hr_hr', verbose_name='发放人'),
        ),
    ]