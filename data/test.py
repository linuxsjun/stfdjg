from web.models import asset_category

#函数
def partt(id):
    tid = asset_category.objects.filter(id=id).first()
    if tid.parentid:
        disname = partt(tid.parentid.id) + '/' +  tid.name
        return disname
    else:
        return tid.name