from django.shortcuts import render, redirect

from django.db.models import Count, Sum

from web.models import hr_hr
from web.models import asset_conf, asset_property, asset_attachment, asset_application
from web.models import hr_department
from web.views import status

import requests, json, time, datetime, hashlib, random

# Create your views here.

def index(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='设备平台'

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

    ps = asset_property.objects.filter(bom=False, active=True, user=signuser).values('id',
    # ps = asset_property.objects.filter(bom=False, active=True).values('id',
                                                                      'status',
                                                                      'sid',
                                                                      'name',
                                                                      'specifications',
                                                                      'warranty',
                                                                      'user__name',
                                                                      'user__active',
                                                                      'asset_attachment__thumbnail',
                                                                      'asset_attachment__final',
                                                                      'user__employee_department__departmentid__name',
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

                try:
                    # 当前设备信息
                    ps = asset_property.objects.get(id=pn)
                except Exception:
                    return redirect('/asset/assetlist/')
                else:
                    context['context'] = ps

                # 设备照片信息
                asspic = asset_attachment.objects.filter(property=pn,active=True, final=True).first()
                if asspic:
                    context['imgid'] = asspic.id
                    context['headimg'] = asspic.thumbnail
                else:
                    # 如果无图则传占位符
                    context['imgid'] = 0
                    context['headimg'] = 'holder.js/64x64'

                user=hr_hr.objects.filter(id=ps.user.id).values('name','employee_department__departmentid__name')
                context['user'] = user.first()
                print(user)

                # ss = asset_property.objects.filter(id=pn).values('id',
                #                                      'asset_attachment__thumbnail',
                #                                      'user__employee_department__departmentid__name')


    # kk = hr_department.objects.all().values('id').annotate(Count('employee_department__employeeid__asset_property__id'),Sum('employee_department__employeeid__asset_property__price'))
    # 'employee_department__employeeid__asset_property__price'
    # print(kk)
    # tt = asset_property.objects.all().values('user','user__name').annotate(Count('id'),Sum('price'))
    # print(tt)
    # ss = asset_property.objects.filter(user=5).values('user','user__name').annotate(Count('id'),Sum('price'))
    # print(ss)
    # s = []
    # for t in list(ps):
    #     # if t['warranty']:
    #     #     t['warranty'] = t['warranty'].strftime("%Y-%m-%d")
    #     # if t['status']:
    #     #     t['statusstr'] = status(t['status'], 2)
    #     # if t['asset_attachment__thumbnail'] == None:
    #     #     t['asset_attachment__thumbnail'] = '/static/img/asset.png'
    #     s.append(t)
    context['context'] = ps
    return render(request, 'assetform.html', context)

def assetappl(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='设备申请'

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

    t = datetime.datetime.now()
    context['now'] = t

    if request.method == "GET":
        print(request.GET)
    elif request.method == "POST":
        print(request.POST)
        if "act" in request.POST:
            if request.POST['act'] == 'create':
                # Todo 新建单据流程->修改单据状态->通知下一流程审批人
                # 提交申请->保存数据

                # 保存数据
                appdate = request.POST['appdate']
                applicant = request.POST['applicant']
                explain = request.POST['explain']
                needasset = request.POST['needasset']
                user = request.POST['user']
                type = request.POST['type']

                backdate =request.POST.get('backdate', '')
                if backdate == '':
                    backdate = None

                item = asset_application(
                    appltno = "ASL325469",
                    applicant = signuser,
                    Explain = request.POST['explain'],
                    type = request.POST['type'],
                    needasset = request.POST['needasset'],
                    backdate = backdate,
                    userhr = signuser,
                    status = 1,
                    flow = 1,
                    active = True,
                )
                item.save()
                item.appltno='ASL{:0>9}'.format(item.id)
                item.save()
    return render(request, 'assetappl.html', context)

def assetprolist(request):
    request.encoding = 'utf-8'
    context = {}
    context['title'] = '审批'

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

    ps = asset_application.objects.filter(applicant=signuser,status=1).values().order_by('-appdate')

    s = []
    for t in list(ps):
        if t['type']:
            if t['type'] == 1:
                t['type'] = '领用'
            if t['type'] == 2:
                t['type'] = '借用'
        if t['status']:
            t['statusstr'] = status(t['status'], 12)
        s.append(t)

    print(s)
    context['processlist'] = s

    ps = asset_application.objects.filter(applicant=signuser).exclude(status=1).values().order_by('-appdate')

    s = []
    for t in list(ps):
        if t['type']:
            if t['type'] == 1:
                t['type'] = '领用'
            if t['type'] == 2:
                t['type'] = '借用'
        if t['status']:
            t['statusstr'] = status(t['status'], 12)
        s.append(t)

    print(s)
    context['overlist'] = s

    return render(request, 'assetprocesslist.html', context)
