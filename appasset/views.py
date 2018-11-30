from django.shortcuts import render

from web.models import hr_hr
from web.models import asset_conf, asset_property

# Create your views here.

def index(request):
    context={}

    return render(request, 'assetbase.html', context)

def assetlist(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='设备列表'

    ps = asset_property.objects.filter(bom=False, active=True).values('id',
                                                                      'status',
                                                                      'sid',
                                                                      'name',
                                                                      'specifications',
                                                                      'warranty',
                                                                      'user__name',
                                                                      'user__active',
                                                                      'asset_attachment__filepath',
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
        if t['asset_attachment__filepath'] == None:
            t['asset_attachment__filepath'] = '/static/img/asset.png'
        s.append(t)
    context['context'] = s
    return render(request, 'assetlist.html', context)