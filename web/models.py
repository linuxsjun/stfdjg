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
    active = models.BooleanField(default=True, verbose_name='有效的')

#==================基本表==================
class base_conf(models.Model):
    #基础设置
    corpid = models.CharField(max_length=128, null=True)
    corpsecret = models.CharField(max_length=64, null=True)
    agentid = models.IntegerField(default=0)
    token = models.CharField(max_length=256, null=True)
    expirestime = models.DateTimeField()

    class Meta:
        db_table = "base_conf"

# class base_flowlist_tpl(models.Model):
#     # 流程
#     formtplid = models.CharField(max_length=16, null=True, verbose_name='模板编号')
#     type = models.IntegerField(default=0, verbose_name='流程类型')
#     sequence = models.IntegerField(default=1, verbose_name='顺序')
#     personnel = models.IntegerField(default=0, verbose_name='签署对象')
#     # 0：个人，1：前级负责人，2：部门/组
#     pertype = models.IntegerField(default=0, verbose_name='对象类型')
#     # 0：会签，1：或签
#     signtype = models.IntegerField(default=0, verbose_name='签署方式')
#     logical = models.CharField(max_length=128, null=True,blank=True, verbose_name='流程逻辑')
#
#     class Meta:
#         db_table = 'base_flowlist_tpl'

class base_flowlist(models.Model):
    # 流程签署记录，由模板生板，具体执行
    formtplid = models.CharField(max_length=16, null=True, verbose_name='模板编号')
    sheet = models.CharField(max_length=16, null=True, verbose_name='单据号')
    type = models.IntegerField(default=0, verbose_name='流程类型')
    sequence = models.IntegerField(default=1, verbose_name='顺序')
    personnel = models.IntegerField(default=0, verbose_name='签署对象')
    # 0：种签，1：或签
    signtype = models.IntegerField(default=0, verbose_name='签署方式')
    confim = models.BooleanField(null=True, blank=True, verbose_name='签署')
    # 不同意必填
    notes = models.TextField(null=True, blank=True, verbose_name='意见')
    confimtime = models.DateTimeField(null=True, blank=True, verbose_name='签署时间')

    class Meta:
        db_table = 'base_flowlist'

class base_menu(models.Model):
    #菜单
    mnid = models.CharField(unique=True, max_length=8, verbose_name='菜单编号')
    name = models.CharField(max_length=16, verbose_name='菜单')
    parentid = models.ForeignKey('self', null=True, blank=True, to_field='mnid', on_delete=models.SET_NULL, verbose_name='上级菜单')
    sequence = models.IntegerField(default=0, verbose_name='顺序')
    linkto = models.CharField(max_length=256, null=True, blank=True, verbose_name='跳转到...')
    active = models.FloatField(default=True, verbose_name='有效的')

    class Meta:
        db_table = 'base_menu'

class base_user_sign_log(models.Model):
    #用户登录日志
    signtime = models.DateTimeField(verbose_name='登录时间')
    employeeid = models.ForeignKey('hr_hr',on_delete=models.CASCADE , verbose_name='员工ID')
    fromip = models.CharField(max_length=16, verbose_name='来源IP')
    contl = models.CharField(max_length=32, verbose_name='描述或登录方式')

    class Meta:
        db_table = "base_user_log"

#==================员工表==================
class hr_department(models.Model):
    #部门表
    pid = models.IntegerField(unique=True)
    name = models.CharField(max_length=32, null=False, verbose_name='名称')
    parentid = models.IntegerField(default=0, verbose_name='上级部门')
    order = models.IntegerField(null=True, verbose_name="次序")
    type = models.IntegerField(default=0, verbose_name='组织类型:0行政/1项目/2团队')

    class Meta:
        db_table = 'hr_department'

class hr_hr(models.Model):
    #员工表employee
    userid = models.CharField(unique=True, max_length=32,verbose_name='用户ID')
    name =  models.CharField(max_length=64,verbose_name='姓名')
    alias =  models.CharField(null=True, blank=True, max_length=32,verbose_name='别名')
    department = models.CharField(null=True, max_length=256,verbose_name='部门')
    position = models.CharField(null=True, max_length=64, verbose_name='职务信息')
    mobile = models.CharField(null=True, max_length=16,verbose_name='手机')
    # 性别，1    表示男性，2    表示女性
    gender = models.CharField(null=True, max_length=16,verbose_name='姓别')
    email = models.EmailField(null=True, verbose_name='邮箱')
    # 头像url。注：如果要获取小图将url最后的”/0”改成”/100”即可。
    avatar = models.CharField(null=True, max_length=256,verbose_name='头像')
    # 激活状态：1 = 已激活    2 = 已禁用    4 = 未激活    已激活代表已激活企业微信或已关注微工作台（原企业号）
    status = models.IntegerField(default=1, verbose_name="激活状态")
    # 成员启用状态。1表示启用的成员，0表示被禁用。服务商调用接口不会返回此字段
    enable = models.IntegerField(default=1, verbose_name="有效")
    # 上级字段，标识是否为上级。0表示普通成员，1表示上级
    isleader = models.IntegerField(default=0,verbose_name='主管')
    extattr = models.CharField(null=True, max_length=256, verbose_name='扩展属性')
    hide_mobile = models.BooleanField(default=0,verbose_name='隐蔽手机')
    english_name = models.CharField(null=True, max_length=64,verbose_name='英文名')
    telephone = models.CharField(null=True, max_length=16,verbose_name='座机')
    order = models.CharField(null=True, max_length=256,verbose_name='部门内的排序值')
    external_profile = models.CharField(null=True, max_length=256,verbose_name='成员对外属性')
    qr_code = models.CharField(null=True, max_length=256,verbose_name='个人二维码')
    passwd = models.CharField(max_length=256,null=True,verbose_name='密码')
    session = models.CharField(max_length=32,null=True,verbose_name='Cookice_session')
    expsession = models.TimeField(null=True)
    # 是否同步企业微信，F未同步，T已同步
    wxsync = models.BooleanField(default=0, verbose_name="同步企业微信")
    active = models.BooleanField(default=True, verbose_name='有效的')

class hr_attr(models.Model):
    # 扩展属性
    # 类型 0：文本 1：网址
    type = models.IntegerField(default=0, verbose_name='类型')
    # 名称
    name = models.TextField(max_length=64, null=True, blank=True, verbose_name='名称')
    # 值
    value = models.TextField(max_length=256, null=True, blank=True, verbose_name='文本')
    url = models.TextField(max_length=256, null=True, blank=True, verbose_name='网址')

    class Meta:
        db_table = 'hr_attr'

class employee_department(models.Model):
    #员工部门表
    employeeid = models.ForeignKey('hr_hr',to_field='userid',on_delete=models.CASCADE , verbose_name='员工ID')
    departmentid = models.ForeignKey('hr_department',to_field='pid', on_delete=models.CASCADE, verbose_name='部门ID')

class hr_conf(models.Model):
    #人力资源配置表
    name = models.CharField(max_length=32, null=True, verbose_name='配置名称')
    agentid = models.IntegerField(null=True, verbose_name='企业微信ID')
    corpsecret = models.CharField(max_length=64,null=True, verbose_name='企业微信密钥')

#==================设备表==================
class asset_application(models.Model):
    #设备领用单->发放单->确认单
    appltno = models.CharField(max_length=16,null=True, blank=True, verbose_name="申请单编号")
    appdate = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    applicant = models.ForeignKey('hr_hr', null=True, blank=True, on_delete=models.SET_NULL, related_name='applicant', verbose_name='申请人')
    Explain = models.TextField(null=True, blank=True, verbose_name='说明')
    needasset = models.CharField(max_length=64, null=True, blank=True, verbose_name='需求')
    type = models.IntegerField(null=True, blank=True, verbose_name='借用/领用')
    backdate = models.DateTimeField(null=True, blank=True, verbose_name="预计时间")
    userhr = models.ForeignKey('hr_hr', null=True, blank=True, on_delete=models.SET_NULL, related_name='user', verbose_name='领用人' )
    # 1审批中；2 已通过；3已驳回；4已取消；6通过后撤销；10已支付
    status = models.IntegerField(default=0, verbose_name='流程状态')
    flow = models.IntegerField(default=0, verbose_name='流程模板号')
    active = models.BooleanField(default=True, verbose_name='有效的')

    class Meta:
        db_table = 'asset_application'

class asset_allot (models.Model):
    # 领用记录
    date = models.DateTimeField(verbose_name="领用时间")
    user = models.ForeignKey('hr_hr', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='领用人')
    parent = models.ForeignKey('asset_application', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='申请单号')
    type = models.IntegerField(null=True, blank=True, verbose_name='借用/领用')
    perreturn = models.DateField(null=True, blank=True, verbose_name="预归还时间")
    assetid = models.ForeignKey('asset_property', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='分配设备')
    managerout = models.ForeignKey('hr_hr', null=True, blank=True, on_delete=models.SET_NULL, related_name='managerout', verbose_name='发放人')
    goreturn = models.DateField(null=True, blank=True, verbose_name="归还时间")
    managerin = models.ForeignKey('hr_hr', null=True, blank=True, on_delete=models.SET_NULL,related_name='managerin', verbose_name='回收人')
    status = models.IntegerField(default=0, verbose_name='流程状态')
    flow = models.IntegerField(default=0, verbose_name='流程模板号')
    active = models.BooleanField(default=True, verbose_name='有效的')

    class Meta:
        db_table = 'asset_allot'

class asset_category(models.Model):
    #设备分类
    name = models.CharField(unique=True, max_length=32, verbose_name='名称')
    parentid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    bom = models.BooleanField(default=False, verbose_name='组件')
    active = models.BooleanField(default=True, verbose_name='有效的')
    notes = models.TextField(null=True, blank=True, verbose_name='备注')
    autosid = models.CharField(max_length=8, null=True, blank=True, verbose_name='自动编号方案')

    class Meta:
        db_table = 'asset_category'

class asset_parts(models.Model):
    #设备配件
    parentid = models.ForeignKey('asset_property',null=True, blank=True, on_delete=models.SET_NULL, verbose_name='归属资产')
    name = models.CharField(max_length=32, verbose_name='名称')
    sn = models.CharField(max_length=32, null=True, verbose_name='出厂编号')
    type = models.CharField(max_length=32, null=True)
    specifications = models.CharField(max_length=64, null=True, verbose_name='规格')
    categoryid = models.ForeignKey('asset_category', null=True, blank=True, on_delete=models.SET_NULL,verbose_name='类型')
    bom = models.BooleanField(default=True, verbose_name='组件')
    price = models.FloatField(default=0, verbose_name='价格')
    purchase = models.DateField(null=True, verbose_name='购买日期')
    wrranty = models.DateField(null=True, verbose_name='维保到期')
    notes = models.TextField(null=True, blank=True, verbose_name='备注')
    status = models.IntegerField(default=1, verbose_name='状态')
    active = models.BooleanField(default=True, verbose_name='有效的')

    class Meta:
        db_table = 'asset_parts'

class asset_property(models.Model):
    #设备表
    sid = models.CharField(max_length=16, unique=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='名称')
    specifications = models.CharField(null=True, blank=True, max_length=64, verbose_name='规格')
    model = models.CharField(null=True, blank=True, max_length=64, verbose_name='型号')
    categoryid = models.ForeignKey('asset_category', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='类型')
    bom = models.BooleanField(default=False, verbose_name='组件')
    purchase = models.DateField(null=True, blank=True, verbose_name='购买日期')
    price = models.FloatField(default=0, verbose_name='价格')
    manufacture = models.DateField(null=True, blank=True, verbose_name='出厂日期')
    warranty = models.DateField(null=True, blank=True, verbose_name='维保到期')
    sn = models.CharField(max_length=32, null=True, blank=True, verbose_name='出厂编号')
    user = models.ForeignKey('hr_hr', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='用户')
    # partlist = models.CharField(max_length=32, null=True, blank=True, verbose_name='配件-多个')
    parentid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='隶属主机')
    position = models.CharField(max_length=24, null=True, blank=True, verbose_name='所在位置')
    status = models.IntegerField(default=1, verbose_name='设备状态')
    nots = models.TextField(null=True, blank=True, verbose_name='备注')
    active = models.BooleanField(default=True, verbose_name='有效的')

    class Meta:
        db_table = 'asset_property'

class asset_conf(models.Model):
    name = models.CharField(max_length=16)
    viewtype = models.IntegerField(default=1, verbose_name='默认显示 1.list 2.board 3.singo')
    listnum = models.IntegerField(default=100, verbose_name='列表每页数')
    boardnum = models.IntegerField(default=50, verbose_name='标签每页数')
    defaultimg = models.CharField(default='/static/img/asset.png',max_length=256, verbose_name='默认图标')

    class Meta:
        db_table = 'asset_conf'

class position(models.Model):
    #设备地址
    name = models.CharField(max_length=32, verbose_name='地址名')
    nots = models.TextField(null=True, verbose_name='备注')

    class Meta:
        db_table = 'base_position'

class asset_attachment(models.Model):
    #设备附件
    property = models.ForeignKey('asset_property', null=True, blank=True, on_delete=models.CASCADE, verbose_name='设备号')
    name = models.CharField(max_length=128, verbose_name='名称')
    filepath = models.CharField(null=True, blank=True, max_length=256, verbose_name='文件路径')
    thumbnail = models.CharField(null=True, blank=True, max_length=256, verbose_name='缩略图')
    oldname = models.CharField(null=True, blank=True, max_length=128, verbose_name='原文件名')
    version = models.IntegerField(default=0, verbose_name='版本号')
    final = models.BooleanField(default=False, verbose_name='终稿标记')
    category = models.CharField(null=True, blank=True, max_length=64, verbose_name='分类')
    nots = models.TextField(null=True, blank=True, verbose_name='备注')
    active = models.BooleanField(default=True, verbose_name='有效的')
    md5 = models.CharField(null=True, blank=True, max_length=32, verbose_name='MD5校验')
    file = models.FileField(null=True, blank=True)

    class Meta:
        db_table = 'asset_attachment'