from django.db import models

# Create your models here.
class pureftp(models.Model):
    status = models.BooleanField(default=1,verbose_name='状态')
    user=models.CharField(max_length=32,verbose_name='账号')
    password=models.CharField(max_length=64,verbose_name='密码')
    uid=models.CharField(max_length=11,verbose_name='用户ID')
    gid=models.CharField(max_length=11,verbose_name='组ID')
    dir=models.CharField(max_length=128,verbose_name='目录')
    ulbandwidth=models.IntegerField(default=0,verbose_name='上传带宽')
    dlbandwidth=models.IntegerField(default=0)
    comment=models.TextField(null=True)
    ipaccess=models.CharField(max_length=15,default='0.0.0.0')
    quotasize=models.IntegerField(default=0)
    quotafiles=models.IntegerField(default=0)
    createdate=models.DateField()
    lastedate=models.DateField()

class base_conf(models.Model):
    corpid = models.CharField(max_length=128, null=True)
    corpsecret = models.CharField(max_length=64, null=True)
    agentid = models.IntegerField(null=True)
    token = models.CharField(max_length=256, null=True)
    expirestime = models.DateTimeField()

    class Meta:
        db_table = "base_conf"

class hr_department(models.Model):
    pid = models.IntegerField(null=False)
    name = models.CharField(max_length=32, null=False)
    parentid = models.IntegerField(null=False,default=0)
    order = models.IntegerField(null=True)

    class Meta:
        db_table = 'hr_department'

class hr_hr(models.Model):
    userid = models.CharField(max_length=32,verbose_name='用户ID')
    name =  models.CharField(max_length=64,verbose_name='姓名')
    department = models.CharField(max_length=256,verbose_name='部门')
    position = models.CharField(max_length=32)
    mobile = models.CharField(max_length=20,verbose_name='手机')
    gender = models.CharField(max_length=16,verbose_name='姓别')
    email = models.EmailField(verbose_name='邮箱')
    avatar = models.CharField(max_length=256,verbose_name='头像')
    status = models.IntegerField(default=1)
    enable = models.IntegerField(default=1)
    isleader = models.IntegerField(default=0,verbose_name='主管')
    extattr = models.CharField(max_length=256)
    hide_mobile = models.BooleanField(default=0,verbose_name='隐蔽手机')
    english_name = models.CharField(max_length=64,verbose_name='英文名')
    telephone = models.CharField(max_length=20,verbose_name='座机')
    order = models.CharField(max_length=256)
    external_profile = models.CharField(max_length=256)
    qr_code = models.CharField(max_length=256,verbose_name='个人二维码')
    passwd = models.CharField(max_length=256,null=True,verbose_name='密码')

