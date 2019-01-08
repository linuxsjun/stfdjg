from django.contrib import admin
from web.models import pureftp, base_conf,  hr_department, hr_hr, employee_department, base_flowlist

from web.models import asset_category, asset_parts, asset_property, asset_application


# Register your models here.
class pueftp_Admin(admin.ModelAdmin):
    list_display = ('user', 'status', 'password', 'uid', 'gid', 'dir', 'ulbandwidth', 'dlbandwidth', 'comment', 'ipaccess', 'quotasize', 'quotafiles', 'createdate', 'lastedate')
admin.site.register(pureftp, pueftp_Admin)

class base_conf_Admin(admin.ModelAdmin):
    list_display = ('corpid', 'corpsecret', 'agentid', 'token', 'expirestime')
admin.site.register(base_conf, base_conf_Admin)

class employee_department_Admin(admin.ModelAdmin):
    list_display = ('employeeid', 'departmentid')
admin.site.register(employee_department, employee_department_Admin)

class hr_department_Admin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'parentid', 'order')
admin.site.register(hr_department, hr_department_Admin)

class hr_hr_Admin(admin.ModelAdmin):
    list_display = ('name','userid', 'department', 'position', 'mobile', 'session', 'active')
admin.site.register(hr_hr, hr_hr_Admin)

class asset_application_Admin(admin.ModelAdmin):
    list_display = ('appltno', 'appdate','applicant', 'Explain', 'status', 'flow', 'active', 'type')
admin.site.register(asset_application, asset_application_Admin)

class asset_category_Admin(admin.ModelAdmin):
    list_display = ('name','parentid', 'bom', 'active')
admin.site.register(asset_category, asset_category_Admin)
admin.site.register(asset_parts)

class asset_property_Admin(admin.ModelAdmin):
    list_display = ('sid', 'name', 'specifications', 'model', 'categoryid', 'purchase', 'price', 'sn', 'status')
admin.site.register(asset_property, asset_property_Admin)

class base_flowlist_Admin(admin.ModelAdmin):
    list_display = ('formtplid', 'sheet', 'type', 'sequence', 'personnel', 'signtype', 'confim', 'notes', 'confimtime')
admin.site.register(base_flowlist, base_flowlist_Admin)
# admin.site.register(asset_property)
