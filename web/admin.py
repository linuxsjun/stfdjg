from django.contrib import admin
from web.models import pureftp, base_conf, hr_department

# Register your models here.
class pueftp_Admin(admin.ModelAdmin):
    list_display = ('user', 'status', 'password', 'uid', 'gid', 'dir', 'ulbandwidth', 'dlbandwidth', 'comment', 'ipaccess', 'quotasize', 'quotaFiles', 'createdate', 'lastedate')

class base_conf_Admin(admin.ModelAdmin):
    list_display = ('corpid', 'corpsecret', 'agentid', 'token', 'expirestime')

class hr_department_Admin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'parentid', 'order')

admin.site.register(pureftp, pueftp_Admin)
admin.site.register(base_conf, base_conf_Admin)
admin.site.register(hr_department, hr_department_Admin)
