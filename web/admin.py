from django.contrib import admin
from web.models import pureftp, base_conf, hr_department, hr_hr, employee_department

# Register your models here.
class pueftp_Admin(admin.ModelAdmin):
    list_display = ('user', 'status', 'password', 'uid', 'gid', 'dir', 'ulbandwidth', 'dlbandwidth', 'comment', 'ipaccess', 'quotasize', 'quotafiles', 'createdate', 'lastedate')

class base_conf_Admin(admin.ModelAdmin):
    list_display = ('corpid', 'corpsecret', 'agentid', 'token', 'expirestime')

class employee_department_Admin(admin.ModelAdmin):
    list_display = ('employeeid', 'departmentid')

class hr_department_Admin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'parentid', 'order')

class hr_hr_Admin(admin.ModelAdmin):
    list_display = ('name','userid', 'department', 'position', 'mobile')

admin.site.register(pureftp, pueftp_Admin)
admin.site.register(base_conf, base_conf_Admin)
admin.site.register(hr_department, hr_department_Admin)
admin.site.register(hr_hr, hr_hr_Admin)
admin.site.register(employee_department, employee_department_Admin)
