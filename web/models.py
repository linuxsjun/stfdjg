from django.db import models

# Create your models here.
class pureftp(models.Model):
    status = models.BooleanField(default=1)
    user=models.CharField(max_length=32)
    password=models.CharField(max_length=64)
    uid=models.CharField(max_length=11)
    gid=models.CharField(max_length=11)
    dir=models.CharField(max_length=128)
    ulbandwidth=models.IntegerField(default=0)
    dlbandwidth=models.IntegerField(default=0)
    comment=models.TextField(null=True)
    ipaccess=models.CharField(max_length=15,default='0.0.0.0')
    quotasize=models.IntegerField(default=0)
    quotaFiles=models.IntegerField(default=0)
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
    usserid = models.CharField(max_length=32)
    name =  models.CharField(max_length=64)
    department = models.CharField(max_length=256)
    position = models.CharField(max_length=32)
    mobile = models.CharField(max_length=18)
    gender = models.BooleanField(default=0)
    email = models.CharField(max_length=128)
    avatar = models.CharField(max_length=256)
    status = models.BooleanField(default=1)
    enable = models.BooleanField(default=1)
    isleader = models.BooleanField(default=0)
    extattr = models.CharField(max_length=256)
    hide_mobile = models.BooleanField(default=0)
    english_name = models.CharField(max_length=64)
    telephone = models.CharField(max_length=18)
    order = models.CharField(max_length=256)
    external_profile = models.CharField(max_length=256)
    qr_code = models.CharField(max_length=256)

