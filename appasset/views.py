from django.shortcuts import render

from web.models import hr_hr
from web.models import asset_conf, asset_property

# Create your views here.

def index(request):
    context={}

    username = request.COOKIES.get('usercookie', None)
    if username:
        try:
            signuser = hr_hr.objects.get(session=username)
        except Exception:
            context['userinfo'] = '用户'
            return render(request, 'sign.html', context)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    return render(request, 'assetbase.html', context)

def assetlist(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='设备列表'

    username = request.COOKIES.get('usercookie', None)
    if username:
        try:
            signuser = hr_hr.objects.get(session=username)
        except Exception:
            context['userinfo'] = '用户'
            return render(request, 'sign.html', context)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    # ps = asset_property.objects.filter(bom=False, active=True, user=signuser).values('id',
    ps = asset_property.objects.filter(bom=False, active=True).values('id',
                                                                      'status',
                                                                      'sid',
                                                                      'name',
                                                                      'specifications',
                                                                      'warranty',
                                                                      'user__name',
                                                                      'user__active',
                                                                      'asset_attachment__thumbnail',
                                                                      'asset_attachment__final',
                                                                      'position',
                                                                      'sn').order_by('name', 'sid')[:50]
    context['spk'] = ps.count()

    s = []
    for t in list(ps):
        if t['warranty']:
            t['warranty'] = t['warranty'].strftime("%Y-%m-%d")
        # if t['status']:
        #     t['statusstr'] = status(t['status'], 2)
        if t['asset_attachment__thumbnail'] == None:
            t['asset_attachment__thumbnail'] = '/static/img/asset.png'
        s.append(t)
    context['context'] = s
    return render(request, 'assetlist.html', context)

def assetform(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='设备详情'

    username = request.COOKIES.get('usercookie', None)
    if username:
        try:
            signuser = hr_hr.objects.get(session=username)
        except Exception:
            context['userinfo'] = '用户'
            return render(request, 'sign.html', context)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    if request.method == "GET":
        print(request.GET)
        if "act" in request.GET:
            if request.GET['act'] == "display":
                context['act'] = "display"
                pn = int(request.GET['id'])
                ps = asset_property.objects.filter(id=pn).values('id',
                                                    'status',
                                                    'sid',
                                                    'name',
                                                    'specifications',
                                                    'warranty',
                                                    'user__name',
                                                    'model',
                                                    'user__active',
                                                    'asset_attachment__thumbnail',
                                                    'asset_attachment__final',
                                                    'position',
                                                    'sn').first()
    context['context'] = ps
    print(context)
    return render(request, 'assetform.html', context)