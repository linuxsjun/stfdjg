from django.db import models

# Create your models here.
class Test(models.Model):
    status = models.BooleanField(default=1)
    user=models.CharField(max_length=32)
    password=models.CharField(max_length=64)
    uid=models.CharField(max_length=11)
    gid=models.CharField(max_length=11)
    dir=models.CharField(max_length=128)
    ulbandwidth=models.IntegerField(max_length=5)
    dlbandwidth=models.IntegerField(max_length=5)
    comment=models.CharField(max_length=128)
    ipaccess=models.CharField(max_length=15)
    quotasize=models.IntegerField(max_length=5)
    quotaFiles=models.IntegerField(max_length=11)
    createdate=models.DateField(auto_now_add=True)
    lastedate=models.DateField()

