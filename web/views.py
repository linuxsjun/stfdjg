from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests, json, time, datetime

import os
from django.conf import settings

from web.models import pureftp, base_conf, hr_department, hr_hr

# Create your views here.

def index(request):
    context={}
    return render(request, 'base.html', context)

def dep_view(request):
    context={}
    context['title']='dep 页面'

    ps = hr_department.objects.all().order_by('pid')
    context['context']= ps

    return render(request, 'view_dep_list.html', context)

def hr_view(request):
    context={}
    context['title']='h 页面'

    # d = base_conf.objects.all().first()
    # ps = hr_department.objects.all().order_by('parentid','order')
    # ps = hr_department.objects.filter(parentid=1).order_by('pid', 'order')
    ps = hr_hr.objects.all().order_by('name')
    context['context']= ps
    return render(request, 'view_hr_list.html', context)

def search_form(request):
    return render_to_response('search_form.html')

def config(request):
    context={}
    context['title']='设置'

    p = base_conf.objects.get(id=1)
    context['context'] = p
    return render(request, 'base_conf.html', context)

def search(request):
    request.encoding='utf-8'
    message={}

    if 'user' in request.GET:
        test = pureftp(createdate='2019-9-9',
                       lastedate='2018-9-8',
                       user=request.GET['user'],
                       password=request.GET['password'])
        # test = pureftp(password=request.GET['password'])
        test.save()
        print("%s -> %s"%(test.user,test.password))
        message['message'] = 'Null->' + test.password + ' ok'
    else:
        message['message']= 'Null'

    # return render(request, 'search.html',message)
    return redirect('/pure_list/')

def view_pure_list(request):
    context={}
    context['title']='pure list'

    ps = pureftp.objects.all()
    context['context'] = ps
    return render(request, 'pure_list.html', context)

def pure_form(request):
    request.encoding='utf-8'
    context={}
    context['title']='pure form'

    if int(request.GET['act']):
        p = pureftp.objects.get(id=request.GET['act'])
        context['context'] = p

    context['act'] = request.GET['act']
    print(context)
    return render(request, 'pure_form.html', context)

def pure_add(request):
    request.encoding = 'utf-8'
    print(request.POST)
    if request.method == "POST":
        if int(request.POST["acte"]):
            #change
            return redirect('/pure_list/')
        else:
            addnew = pureftp(
                status = 1,
                user = str(request.POST['user']),
                password = str(request.POST['password']),
                ipaccess = str(request.POST['ipaccess']),
                dir = str(request.POST['dir']),
                uid = str(request.POST['uid']),
                gid = str(request.POST['gid']),
                ulbandwidth = str(request.POST['ulbandwidth']),
                dlbandwidth = str(request.POST['dlbandwidth']),
                quotasize = str(request.POST['quotasize']),
                quotafiles = str(request.POST['quotafiles']),
                createdate = str(request.POST['createdate']),
                lastedate = str(request.POST['lastedate']),
                comment = str(request.POST['comment']))
            addnew.save()
            return redirect('/pure_list/')

def getToken(request):
    # list = pureftp.objects.all()
    # d = base_conf.objects.all().first()
    # d=base_conf.objects.filter(id=1)

    # d=base_conf.objects.get(id=1)
    d = base_conf.objects.get(pk=1)

    # pureftp.objects.order_by("id")

    #https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRECT
    # corpid=ww74c5af840cdd5cb6
    # corpsecret=uUJf-eFplyKlAWf2Cc9T8Guea4K1zpEiZXwXpCsHTQs

    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    v = {}
    v['corpid'] = d.corpid
    v['corpsecret'] = d.corpsecret

    r = requests.get(url, params=v)
    t = json.loads(r.text)

    if t['errcode'] == 0:
        d.token = t['access_token']
        print(len(t['access_token']))

        tt = time.time()
        d.expirestime = datetime.datetime.fromtimestamp(tt + t['expires_in'])

        d.save()
        response = "GET Token ID is ok at %s"%d.expirestime
    else:
        response = "No"
    return HttpResponse(response)

def readdepartment(request):
    p =  base_conf.objects.all().first()

    # https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=ACCESS_TOKEN&id=ID
    url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list'
    v = {}
    v['access_token'] = p.token
    v['id'] = p.corpsecret

    try:
        r = requests.get(url, params=v)
    except Exception:
        print('get url is error')
    else:
        t = json.loads(r.text)
        if t['errcode'] == 0:
            d ={}
            for d in t['department']:
                dt = hr_department(pid=d['id'],
                                   name=d['name'],
                                   parentid=d['parentid'],
                                   order=d['order'])
                print(d)
                dt.save()
        response = t
    return redirect('/dep/')

def gethr(request):
    p =  base_conf.objects.all().first()

    # https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token=ACCESS_TOKEN&department_id=DEPARTMENT_ID&fetch_child=FETCH_CHILD
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/list'
    # https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=ACCESS_TOKEN&department_id=DEPARTMENT_ID&fetch_child=FETCH_CHILD
    # url = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist'
    v = {}
    v['access_token'] = p.token
    v['department_id'] = p.department_id =1
    v['fetch_child'] = 1

    r = requests.get(url, params=v)
    t = json.loads(r.text)

    if t['errcode'] == 0:
        d = {}
        for d in t['userlist']:
            dt = hr_hr(userid=d['userid'],
                       name=d['name'],
                       department=d['department'],
                       position=d['position'],
                       mobile=d['mobile'],
                       gender=d['gender'],
                       email=d['email'],
                       avatar=d['avatar'],
                       status=d['status'],
                       enable=d['enable'],
                       isleader=d['isleader'],
                       extattr=d['extattr'],
                       hide_mobile=d['hide_mobile'],
                       english_name=d['english_name'],
                       telephone=d['telephone'],
                       order=d['order'],
                       # external_profile=d['external_profile'],
                       qr_code=d['qr_code'])
            dt.save()
    return redirect('/hr/')

def uploadfile(request):
    if request.method == "POST":
        f = request.FILES["file"]
        filePath = os.path.join(settings.MDEIA_ROOT, f.name)
        print(filePath)
        i=0
        with open(filePath,'wb') as fp:
            for info in f.chunks():
                i = i + 1
                print (i)
                fp.write(info)
        return HttpResponse('ok')
    else:
        return HttpResponse('no')