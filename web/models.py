from django.db import models

# Create your models here.
class pureftp(models.Model):
    #pureFtp用户表
    status = models.BooleanField(default=1,verbose_name='状态')
    user=models.CharField(max_length=32,verbose_name='账号')
    password=models.CharField(max_length=64,verbose_name='密码')
    uid=models.CharField(max_length=11,verbose_name='用户ID')
    gid=models.CharField(max_length=11,verbose_name='组ID')
    dir=models.CharField(max_length=128,verbose_name='目录')
    ulbandwidth=models.IntegerField(default=0,verbose_name='上传带宽')
    dlbandwidth=models.IntegerField(default=0)
    comment=models.TextField(blank=True)
    ipaccess=models.CharField(max_length=15,default='0.0.0.0')
    quotasize=models.IntegerField(default=0)
    quotafiles=models.IntegerField(default=0)
    createdate=models.DateField()
    lastedate=models.DateField()

class base_conf(models.Model):
    #基础设置
    corpid = models.CharField(max_length=128, blank=True)
    corpsecret = models.CharField(max_length=64, blank=True)
    agentid = models.IntegerField(blank=True, default=0)
    token = models.CharField(max_length=256, blank=True)
    expirestime = models.DateTimeField()

    class Meta:
        db_table = "base_conf"

class base_user_sign_log(models.Model):
    #用户登录日志
    signtime = models.DateTimeField(verbose_name='登录时间')
    employeeid = models.ForeignKey('hr_hr',on_delete=models.CASCADE , verbose_name='员工ID')
    fromip = models.CharField(max_length=16, verbose_name='来源IP')
    contl = models.CharField(max_length=32, verbose_name='描述')

class hr_department(models.Model):
    #部门表
    pid = models.IntegerField(unique=True)
    name = models.CharField(max_length=32, null=False, verbose_name='名称')
    parentid = models.IntegerField(blank=True,default=0, verbose_name='上级部门')
    order = models.IntegerField(blank=True)

    class Meta:
        db_table = 'hr_department'

class hr_hr(models.Model):
    #员工表
    userid = models.CharField(unique=True, max_length=32,verbose_name='用户ID')
    name =  models.CharField(max_length=64,verbose_name='姓名')
    department = models.CharField(blank=True, max_length=256,verbose_name='部门')
    position = models.CharField(blank=True, max_length=32)
    mobile = models.CharField(blank=True, max_length=20,verbose_name='手机')
    gender = models.CharField(blank=True, max_length=16,verbose_name='姓别')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    avatar = models.CharField(blank=True, max_length=256,verbose_name='头像')
    status = models.IntegerField(blank=True, default=1)
    enable = models.IntegerField(blank=True, default=1)
    isleader = models.IntegerField(blank=True, default=0,verbose_name='主管')
    extattr = models.CharField(blank=True, max_length=256, verbose_name='扩展属性')
    hide_mobile = models.BooleanField(blank=True, default=0,verbose_name='隐蔽手机')
    english_name = models.CharField(blank=True, max_length=64,verbose_name='英文名')
    telephone = models.CharField(blank=True, max_length=20,verbose_name='座机')
    order = models.CharField(blank=True, max_length=256)
    external_profile = models.CharField(blank=True, max_length=256)
    qr_code = models.CharField(blank=True, max_length=256,verbose_name='个人二维码')
    passwd = models.CharField(blank=True, max_length=256,null=True,verbose_name='密码')
    session = models.CharField(blank=True, max_length=16,null=True,verbose_name='Cookice_session')
    expsession = models.TimeField(blank=True,null=True)

class employee_department(models.Model):
    #员工部门表
    employeeid = models.ForeignKey('hr_hr',to_field='userid',on_delete=models.CASCADE , verbose_name='员工ID')
    departmentid = models.ForeignKey('hr_department',to_field='pid', on_delete=models.CASCADE, verbose_name='部门ID')

class hr_conf(models.Model):
    #人力资源配置表
    name = models.CharField(max_length=32, blank=True, verbose_name='配置名称')
    agentid = models.IntegerField(blank=True, verbose_name='企业微信ID')
    corpsecret = models.CharField(max_length=64,blank=True, verbose_name='企业微信密钥')

