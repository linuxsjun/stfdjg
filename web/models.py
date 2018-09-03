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
    comment=models.TextField(null=True)
    ipaccess=models.CharField(max_length=15,default='0.0.0.0')
    quotasize=models.IntegerField(default=0)
    quotafiles=models.IntegerField(default=0)
    createdate=models.DateField()
    lastedate=models.DateField()

class base_conf(models.Model):
    #基础设置
    corpid = models.CharField(max_length=128, null=True)
    corpsecret = models.CharField(max_length=64, null=True)
    agentid = models.IntegerField(default=0)
    token = models.CharField(max_length=256, null=True)
    expirestime = models.DateTimeField()

    class Meta:
        db_table = "base_conf"

class base_menu(models.Model):
    #菜单
    name = models.CharField(max_length=16, verbose_name='菜单')
    nameid = models.CharField(unique=True, max_length=8, verbose_name='菜单编号')
    parentid = models.ForeignKey('self', null=True, blank=True, to_field='nameid', on_delete=models.SET_NULL, verbose_name='上级菜单')
    status = models.FloatField(default=True)

    class Meta:
        db_table = 'base_menu'

class base_user_sign_log(models.Model):
    #用户登录日志
    signtime = models.DateTimeField(verbose_name='登录时间')
    employeeid = models.ForeignKey('hr_hr',on_delete=models.CASCADE , verbose_name='员工ID')
    fromip = models.CharField(max_length=16, verbose_name='来源IP')
    contl = models.CharField(max_length=32, verbose_name='描述或登录方式')

class hr_department(models.Model):
    #部门表
    pid = models.IntegerField(unique=True)
    name = models.CharField(max_length=32, null=False, verbose_name='名称')
    parentid = models.IntegerField(default=0, verbose_name='上级部门')
    order = models.IntegerField(null=True)

    class Meta:
        db_table = 'hr_department'

class hr_hr(models.Model):
    #员工表
    userid = models.CharField(unique=True, max_length=32,verbose_name='用户ID')
    name =  models.CharField(max_length=64,verbose_name='姓名')
    department = models.CharField(null=True, max_length=256,verbose_name='部门')
    position = models.CharField(null=True, max_length=32)
    mobile = models.CharField(null=True, max_length=16,verbose_name='手机')
    gender = models.CharField(null=True, max_length=16,verbose_name='姓别')
    email = models.EmailField(null=True, verbose_name='邮箱')
    avatar = models.CharField(null=True, max_length=256,verbose_name='头像')
    status = models.IntegerField(default=1)
    enable = models.IntegerField(default=1)
    isleader = models.IntegerField(default=0,verbose_name='主管')
    extattr = models.CharField(null=True, max_length=256, verbose_name='扩展属性')
    hide_mobile = models.BooleanField(default=0,verbose_name='隐蔽手机')
    english_name = models.CharField(null=True, max_length=64,verbose_name='英文名')
    telephone = models.CharField(null=True, max_length=16,verbose_name='座机')
    order = models.CharField(null=True, max_length=256)
    external_profile = models.CharField(null=True, max_length=256)
    qr_code = models.CharField(null=True, max_length=256,verbose_name='个人二维码')
    passwd = models.CharField(max_length=256,null=True,verbose_name='密码')
    session = models.CharField(max_length=32,null=True,verbose_name='Cookice_session')
    expsession = models.TimeField(null=True)


class employee_department(models.Model):
    #员工部门表
    employeeid = models.ForeignKey('hr_hr',to_field='userid',on_delete=models.CASCADE , verbose_name='员工ID')
    departmentid = models.ForeignKey('hr_department',to_field='pid', on_delete=models.CASCADE, verbose_name='部门ID')

class hr_conf(models.Model):
    #人力资源配置表
    name = models.CharField(max_length=32, null=True, verbose_name='配置名称')
    agentid = models.IntegerField(null=True, verbose_name='企业微信ID')
    corpsecret = models.CharField(max_length=64,null=True, verbose_name='企业微信密钥')

class asset_category(models.Model):
    #设备分类
    name = models.CharField()
    parentid = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    bom = models.BooleanField()
    active = models.BooleanField(verbose_name='删除状况')

    class Meta:
        db_table = 'asset_category'

class asset_parts(models.Model):
    #设备配件
    parentid = models.ForeignKey('asset_property',on_delete=models.SET_NULL)
    name = models.CharField()
    sn = models.CharField()
    type = models.CharField()
    specifications = models.CharField()
    bom = models.BooleanField()
    price = models.FloatField()
    purchase = models.DateField()
    wrranty = models.DateField()
    notes = models.TextField()
    status = models.IntegerField(verbose_name='状态')
    active = models.BooleanField(verbose_name='删除状况')

    class Meta:
        db_table = 'asset_parts'

class asset_property(models.Model):
    #设备表
    sid = models.CharField()
    name = models.CharField()
    specifications = models.CharField()
    model = models.CharField()
    typeid = models.ForeignKey('asset_category', on_delete=models.SET_NULL)
    purchase = models.DateField()
    price = models.FloatField()
    manufacture = models.DateField()
    warranty = models.DateField()
    sn = models.CharField(verbose_name='出厂编号')
    user = models.ForeignKey('hr_hr', on_delete=models.SET_NULL, verbose_name='用户')
    partlist = models.CharField(verbose_name='配件-多个')
    status = models.IntegerField(verbose_name='设备状态')
    nots = models.TextField(verbose_name='备注')
    active = models.BooleanField(verbose_name='是否删除')

    class Meta:
        db_table = 'asset_property'

class position(models.Model):
    #设备地址
    name = models.CharField(verbose_name='地址名')