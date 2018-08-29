# Generated by Django 2.1 on 2018-08-24 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='hr_conf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, null=True)),
                ('agentid', models.IntegerField(null=True)),
                ('corpsecret', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='hr_hr',
            name='session',
            field=models.CharField(max_length=256, null=True, verbose_name='Cookice_session'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='avatar',
            field=models.CharField(max_length=256, verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='department',
            field=models.CharField(max_length=256, verbose_name='部门'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='english_name',
            field=models.CharField(max_length=64, verbose_name='英文名'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='gender',
            field=models.CharField(max_length=16, verbose_name='姓别'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='hide_mobile',
            field=models.BooleanField(default=0, verbose_name='隐蔽手机'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='isleader',
            field=models.IntegerField(default=0, verbose_name='主管'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='mobile',
            field=models.CharField(max_length=20, verbose_name='手机'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='name',
            field=models.CharField(max_length=64, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='passwd',
            field=models.CharField(max_length=256, null=True, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='qr_code',
            field=models.CharField(max_length=256, verbose_name='个人二维码'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='telephone',
            field=models.CharField(max_length=20, verbose_name='座机'),
        ),
        migrations.AlterField(
            model_name='hr_hr',
            name='userid',
            field=models.CharField(max_length=32, verbose_name='用户ID'),
        ),
        migrations.AlterField(
            model_name='pureftp',
            name='dir',
            field=models.CharField(max_length=128, verbose_name='目录'),
        ),
        migrations.AlterField(
            model_name='pureftp',
            name='gid',
            field=models.CharField(max_length=11, verbose_name='组ID'),
        ),
        migrations.AlterField(
            model_name='pureftp',
            name='password',
            field=models.CharField(max_length=64, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='pureftp',
            name='status',
            field=models.BooleanField(default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='pureftp',
            name='uid',
            field=models.CharField(max_length=11, verbose_name='用户ID'),
        ),
        migrations.AlterField(
            model_name='pureftp',
            name='ulbandwidth',
            field=models.IntegerField(default=0, verbose_name='上传带宽'),
        ),
        migrations.AlterField(
            model_name='pureftp',
            name='user',
            field=models.CharField(max_length=32, verbose_name='账号'),
        ),
    ]