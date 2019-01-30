from django.db import models

# Create your models here.
#==================基本表==================
class pro_conf(models.Model):
    #基础设置
    name = models.CharField(max_length=16)
    viewtype = models.IntegerField(default=1, verbose_name='默认显示 1.list 2.board 3.singo')
    listnum = models.IntegerField(default=100, verbose_name='列表每页数')
    boardnum = models.IntegerField(default=50, verbose_name='标签每页数')
    defaulturl = models.CharField(default='/static/upfile/project/',max_length=256, verbose_name='默认文件目录')

    class Meta:
        db_table = "pro_conf"