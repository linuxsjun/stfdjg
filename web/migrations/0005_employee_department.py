# Generated by Django 2.1 on 2018-08-30 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_hr_hr_expsession'),
    ]

    operations = [
        migrations.CreateModel(
            name='employee_department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeid', models.IntegerField(verbose_name='员工ID')),
                ('department', models.IntegerField(verbose_name='部门ID')),
            ],
        ),
    ]
