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
    comment=models.CharField(max_length=128)
    ipaccess=models.CharField(max_length=15,default='0.0.0.0')
    quotasize=models.IntegerField(default=0)
    quotaFiles=models.IntegerField(default=0)
    createdate=models.DateField()
    lastedate=models.DateField()

class base_conf(models.Model):
    corpid = models.CharField(max_length=128, )
    corpsecret = models.CharField(max_length=64)
    agentid = models.IntegerField()
    token = models.CharField(max_length=256)
    expirestime = models.DateTimeField()

    class Meta:
        db_table = "base_conf"
