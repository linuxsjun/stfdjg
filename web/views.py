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
    username = request.COOKIES.get('username', '')
    #TODO 判断COOKIE的方式有问题，无这一COOKIE用户的情况下就会ERROR
    if username:
        signuser = hr_hr.objects.get(userid=username)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)
    return render(request, 'base.html', context)

def dep_view(request):
    context={}
    context['title']='部门'

    username = request.COOKIES.get('username', '')
    if username:
        signuser = hr_hr.objects.get(userid=username)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    ps = hr_department.objects.all().order_by('pid')
    context['context']= ps
    return render(request, 'view_dep_list.html', context)

def hr_view(request):
    context={}
    context['title']='人员'

    username = request.COOKIES.get('username', '')
    if username:
        signuser = hr_hr.objects.get(userid=username)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    # d = base_conf.objects.all().first()
    # ps = hr_department.objects.all().order_by('parentid','order')
    # ps = hr_department.objects.filter(parentid=1).order_by('pid', 'order')
    ps = hr_hr.objects.all().order_by('name')
    context['context']= ps
    return render(request, 'view_hr_list.html', context)

def sign_view(request):
    context={}
    context['userinfo'] = '登录'
    context['stat'] = 'CLItMYby44wD8vgM'
    request.encoding = 'utf-8'
    if request.method == "POST":
        if request.POST["user"]:
            seluser = request.POST['user']
            users = hr_hr.objects.filter(userid = seluser)
            if users:
                gourl = redirect('/')
                gourl.set_cookie('username',seluser,3600)
                return gourl
    elif request.method == "GET":
        if 'code' in request.GET:
            if request.GET['code']:
                code = request.GET['code']

                url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
                v = {}
                v['corpid'] = 'ww74c5af840cdd5cb6'
                v['corpsecret'] = 'HBzQYMHZHw1UwQcqDI8GBsTnTTRJA_ODkgZuo2QuT28'

                r = requests.get(url, params=v)
                t = json.loads(r.text)

                url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo'
                v = {}
                v['access_token'] = t['access_token']
                v['code'] = code

                r = requests.get(url, params=v)
                t = json.loads(r.text)

                seluser = t['UserId']
                users = hr_hr.objects.filter(userid=seluser)
                if users:
                    gourl = redirect('/')
                    gourl.set_cookie('username', seluser, 3600)
                    return gourl
        else:
            print('code is no')

    return render(request, 'sign.html', context)

def signout(request):
    username = request.COOKIES.get('username', '')
    try:
        gourl = redirect('/')
        gourl.delete_cookie('username')
        return gourl
    except Exception:
        return redirect('/')
    return redirect('/')

def config(request):
    context={}
    context['title']='设置'

    username = request.COOKIES.get('username', '')
    if username:
        signuser = hr_hr.objects.get(userid=username)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    p = base_conf.objects.get(id=1)
    context['context'] = p
    return render(request, 'base_conf.html', context)

def search(request):
    context={}
    context['title']='pure list'

    username = request.COOKIES.get('username', '')
    if username:
        signuser = hr_hr.objects.get(userid=username)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    return render(request, 'search.html',context)

def view_pure_list(request):
    context={}
    context['title']='pure list'

    username = request.COOKIES.get('username', '')
    if username:
        signuser = hr_hr.objects.get(userid=username)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    ps = pureftp.objects.all()
    context['context'] = ps
    return render(request, 'pure_list.html', context)

def pure_form(request):
    request.encoding='utf-8'
    context={}
    context['title']='表单'

    username = request.COOKIES.get('username', '')
    if username:
        signuser = hr_hr.objects.get(userid=username)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    if int(request.GET['act']):
        p = pureftp.objects.get(id=request.GET['act'])
        context['context'] = p
    else:
        cdate = datetime.date.fromtimestamp(time.time())
        ldate = datetime.date.fromtimestamp(time.time())

        p = {'status': 'true',
             'ipaccess': '0.0.0.0',
             'uid': 1001,
             'gid': 1001,
             'ulbandwidth': 0,
             'dlbandwidth': 0,
             'quotasize': 0,
             'quotafiles': 0,
             'createdate': cdate,
             'lastedate': ldate}

        context['context'] = p

    context['act'] = request.GET['act']
    return render(request, 'pure_form.html', context)

def pure_add(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        if int(request.POST["acte"]):
            cid = int((request.POST["acte"]))

            if 'status' in request.POST:
                cstatus = 1
            else:
                cstatus = 0
            cuser = str(request.POST['user'])
            cpassword = str(request.POST['password'])
            cipaccess = str(request.POST['ipaccess'])
            cdir = str(request.POST['dir'])
            cuid = str(request.POST['uid'])
            cgid = str(request.POST['gid'])
            culbandwidth = int(request.POST['ulbandwidth'])
            cdlbandwidth = int(request.POST['dlbandwidth'])
            cquotasize = int(request.POST['quotasize'])
            cquotafiles = int(request.POST['quotafiles'])
            ccomment = str(request.POST['comment'])

            pureftp.objects.filter(id=cid).update(status = cstatus,
                                                  user = cuser,
                                                  password = cpassword,
                                                  ipaccess = cipaccess,
                                                  dir = cdir,
                                                  uid = cuid,
                                                  gid = cgid,
                                                  ulbandwidth = culbandwidth,
                                                  dlbandwidth = cdlbandwidth,
                                                  quotafiles = cquotafiles,
                                                  quotasize = cquotasize,
                                                  comment = ccomment)
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
                ulbandwidth = int(request.POST['ulbandwidth']),
                dlbandwidth = int(request.POST['dlbandwidth']),
                quotasize = int(request.POST['quotasize']),
                quotafiles = int(request.POST['quotafiles']),
                createdate = str(request.POST['createdate']),
                lastedate = str(request.POST['lastedate']),
                comment = str(request.POST['comment']))
            addnew.save()
            return redirect('/pure_list/')

def pure_del(request):
    request.encoding='utf-8'
    context={}
    context['title']='pure form'

    print("aaaaa")
    if "act" in request.GET:
        delid = int(request.GET['id'])
        delitem = pureftp.objects.get(id=delid)
        delitem.delete()

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
        with open(filePath,'wb') as fp:
            for info in f.chunks():
                fp.write(info)
        return HttpResponse('ok')
    else:
        return HttpResponse('no')

def test(request):
    v = {}
    v['access_token'] = 'PP-YvltOWYOlkz28puKRqlCIA8pkrGy2X-qMapexdjz-2-CmRA8eteyZ1g2rUzu5IWS3lnmoIHX1nR5EZTEKJb2RR6WroAR-KHvl0Zl3Al886Ny-pySOqkP8obzTQlw1ipMVRTZ1wAGpXW3vt3mLCTkCCo2unZ5f_oPjZzRmU100QOTEmWyB3a0Zi50uwVk5BNzk9YP8PSK-wlNdWFkheQ'
    txt = {"touser" : "SunJun",
               "msgtype" : "text",
               "agentid" : 1000013,
               "text" : {
                   "content" : "测试消息\n文本内容<a href=\"http://work.weixin.qq.com\">网页链接</a>，请勿回复。"},
               "safe":1
               }
    # jsontxt = json.dumps(context)
    print(txt)

    urls = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
    r = requests.post(urls,params=v,json=txt)

    return HttpResponse(r.text)