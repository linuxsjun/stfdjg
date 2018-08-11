from django.contrib import admin
from web.models import pureftp, base_conf

# Register your models here.
class pueftp_Admin(admin.ModelAdmin):
    list_display = ('user',
                    'status',
                    'password',
                    'uid',
                    'gid',
                    'dir',
                    'ulbandwidth',
                    'dlbandwidth',
                    'comment',
                    'ipaccess',
                    'quotasize',
                    'quotaFiles',
                    'createdate',
                    'lastedate')

class base_conf_Admin(admin.ModelAdmin):
    list_display = ('corpid', 'corpsecret', 'agentid', 'token', 'expirestime')

admin.site.register(pureftp, pueftp_Admin)
admin.site.register(base_conf, base_conf_Admin)
