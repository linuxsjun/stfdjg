# Generated by Django 2.1.1 on 2018-10-23 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_auto_20181023_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='hr_hr',
            name='alias',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='别名'),
        ),
        migrations.AlterField(
            model_name='hr_department',
            name='order',
            field=models.IntegerField(null=True, verbose_name='次序'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='external_profile',
            field=models.CharField(max_length=256, null=True, verbose_name='成员对外属性'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='order',
            field=models.CharField(max_length=256, null=True, verbose_name='部门内的排序值'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='position',
            field=models.CharField(max_length=32, null=True, verbose_name='职务信息'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='status',
            field=models.IntegerField(default=1, verbose_name='激活状态:1已激活2已禁用4未激活'),
        ),
    ]