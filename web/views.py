from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import render_to_response
import requests, json, time, datetime, hashlib, random

# from data.test import *

import os
import re
from django.conf import settings

from web.models import pureftp, base_conf, hr_department, hr_hr, employee_department, base_user_sign_log
from web.models import asset_conf, asset_category, asset_parts, asset_property, position, asset_attachment

from openpyxl import load_workbook

def partt(id):
    #这是一个定义函数，返回父级关系
    tid = asset_category.objects.filter(id=id).first()
    if tid.parentid:
        disname = partt(tid.parentid.id) + ' / ' +  tid.name
        return disname
    else:
        return tid.name

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

    return render(request, 'base.html', context)

def category_list(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='category_list'

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

    print(request.method)
    if request.method == "GET":
        if "act" in request.GET:
            if request.GET['act'] == 'sort':
                pass
        else:
            ps = asset_category.objects.all().order_by('parentid')
            lcats = []
            for cat in ps:
                ncat = {}
                ncat["id"] = cat.id
                ncat["name"] = cat.name
                ncat["bom"] = cat.bom
                if cat.parentid:
                    ncat["displayname"] = partt(cat.parentid.id)
                else:
                    ncat["displayname"] =" "
                lcats.append(ncat)
            context['context'] = lcats

    return render(request, 'category_list.html', context)

def dep_view(request):
    context={}
    context['title']='部门'

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

    ps = hr_department.objects.all().order_by('pid')
    context['context']= ps
    return render(request, 'view_dep_list.html', context)

def hr_view(request):
    context={}
    context['title']='人员'

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

    # d = base_conf.objects.all().first()
    # ps = hr_department.objects.all().order_by('parentid','order')
    # ps = hr_department.objects.filter(parentid=1).order_by('pid', 'order')
    ps = hr_hr.objects.filter(active=True).order_by('name')
    context['context']= ps
    return render(request, 'view_hr_broad.html', context)

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
                u = users.first()
                rnd = seluser + str(time.time()) + str(random.randint(10000,20000))
                strsession = hashlib.md5()
                strsession.update(rnd.encode('utf-8'))
                s = strsession.hexdigest()
                u.session = s
                u.save()

                #登录日志
                wlog = base_user_sign_log(signtime = datetime.datetime.fromtimestamp(time.time()),
                                          employeeid = u,
                                          fromip = request.META.get('REMOTE_ADDR','0.0.0.0'),
                                          contl = 'user&passwd')
                wlog.save()

                gourl = redirect('/')
                gourl.set_cookie('usercookie',s,14400)

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
                    u = users.first()
                    rnd = seluser + str(time.time()) + str(random.randint(10000, 20000))
                    strsession = hashlib.md5()
                    strsession.update(rnd.encode('utf-8'))
                    s = strsession.hexdigest()
                    u.session = s
                    u.save()

                    # 登录日志
                    wlog = base_user_sign_log(signtime=datetime.datetime.fromtimestamp(time.time()),
                                              employeeid=u,
                                              fromip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
                                              contl='Scan WX-code')
                    wlog.save()

                    gourl = redirect('/')
                    gourl.set_cookie('usercookie', s, 14400)
                    return gourl
        else:
            print('code is no')

    return render(request, 'sign.html', context)

def signout(request):
    username = request.COOKIES.get('usercookie', None)
    try:
        signuser = hr_hr.objects.get(session=username)
        signuser.session = '0000000000000000'
        # signuser.expsession = 0
        signuser.save()

        gourl = redirect('/')
        gourl.delete_cookie('username')
        return gourl
    except Exception:
        return redirect('/')
    return redirect('/')

def config(request):
    context={}
    context['title']='设置'

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

    p = base_conf.objects.get(id=1)
    context['context'] = p
    return render(request, 'base_conf.html', context)

def view_pure_list(request):
    context={}
    context['title']='pure list'

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

    ps = pureftp.objects.all().order_by('-id')
    context['context'] = ps
    return render(request, 'pure_list.html', context)

def pure_form(request):
    request.encoding='utf-8'
    context={}
    context['title']='表单'

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

    if "act" in request.GET:
        delid = int(request.GET['id'])
        delitem = pureftp.objects.get(id=delid)
        delitem.delete()

    return redirect('/pure_list/')

def getToken(request):
    if "act" in request.GET:
        if request.GET['act'] == 'gettoken':
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
                response = d.token
            else:
                response = "Error"

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
            print('-----------------')
            try:
                chkem=None
                chkem = hr_hr.objects.filter(userid=d['userid'])
            except Exception:
                print('chkem error')
                pass
            if chkem:
                #记录已存在
                pass
            else:
                #-----------------
                u_userid = d['userid']
                u_name = d['name']
                u_position = d['position']
                u_mobile = d['mobile']
                u_gender = d['gender']
                u_email = d['email']
                u_avatar = d['avatar']
                u_status = d['status']
                u_enable = d['enable']
                u_isleader = d['isleader']
                u_extattr = d['extattr']
                u_hide_mobile = d['hide_mobile']
                u_english_name = d['english_name']
                u_telephone = d['telephone']
                u_order = d['order']
                # u_external_profile=d['external_profile']
                u_qr_code = d['qr_code']
                #-----------------

                dt = hr_hr(userid=d['userid'],
                           name=u_name,
                           position=u_position,
                           mobile=u_mobile,
                           gender=u_gender,
                           email=u_email,
                           avatar=u_avatar,
                           status=u_status,
                           enable=u_enable,
                           isleader=u_isleader,
                           extattr=u_extattr,
                           hide_mobile=u_hide_mobile,
                           english_name=u_english_name,
                           telephone=u_telephone,
                           order=u_order,
                           # external_profile=u_external_profile,
                            qr_code=u_qr_code)
                dt.save()
                print(u_name)

                #关联员工与部门
                nemp = hr_hr.objects.get(userid=d['userid'])
                ds = d['department']

                for de in ds:
                    des = int(de)
                    try:
                        dep = hr_department.objects.filter(pid=des).first()
                    except Exception:
                        pass
                    else:
                        try:
                            rep = employee_department.objects.filter(employeeid=nemp.userid,departmentid=des)
                        except Exception:
                            pass
                        else:
                            if len(rep):
                                pass
                            else:
                                seds = employee_department(employeeid=nemp,departmentid=dep)
                                seds.save()

    return redirect('/hr/')

def uploadfile(request):
    print(request.POST)
    if request.method == "POST":
        f = request.FILES["file"]
        # filePath = os.path.join(settings.MDEIA_ROOT, f.name)
        filePath = os.path.join(settings.MDEIA_ROOT, f.name)
        print(filePath)
        with open(filePath,'wb') as fp:
            for info in f.chunks():
                fp.write(info)
        return HttpResponse('ok')
    else:
        return HttpResponse('no')

def sendmsg(request):
    v = {}
    v['access_token'] = 'PP-YvltOWYOlkz28puKRqlCIA8pkrGy2X-qMapexdjz-2-CmRA8eteyZ1g2rUzu5IWS3lnmoIHX1nR5EZTEKJb2RR6WroAR-KHvl0Zl3Al886Ny-pySOqkP8obzTQlw1ipMVRTZ1wAGpXW3vt3mLCTkCCo2unZ5f_oPjZzRmU100QOTEmWyB3a0Zi50uwVk5BNzk9YP8PSK-wlNdWFkheQ'
    txt = {"touser" : "SunJun",
               "msgtype" : "text",
               "agentid" : 1000013,
               "text" : {
                   "content" : "测试消息\n文本内容<a href=\"http://work.weixin.qq.com\">网页链接</a>，请勿回复。"},
               "safe":0
               }
    # jsontxt = json.dumps(context)
    print(txt)

    urls = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
    r = requests.post(urls,params=v,json=txt)

    return HttpResponse(r.text)

def wxdoor(request):
    # url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    # v = {}
    # v['corpid'] = 'ww74c5af840cdd5cb6'
    # v['corpsecret'] = 'HBzQYMHZHw1UwQcqDI8GBsTnTTRJA_ODkgZuo2QuT28'
    #
    # r = requests.get(url, params=v)
    # t = json.loads(r.text)
    # print(t['access_token'])
    #
    # context = t['access_token']

    # print(request.text)
    # v = {}
    # url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
    # v['appid'] = 'ww74c5af840cdd5cb6'
    # v['redirect_uri'] = '172.18.0.231:8000'
    # v['response_type'] = 'code'
    # v['scope'] = 'snsapi_base'
    # v['agentid'] = '1000013'
    # v['state'] =  ''
    # r = requests.get(url, params=v)

    # print(request.method)
    # print(request.GET)
    # print(request.COOKIES)
    # g = get hr_hr.objects

    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=ww74c5af840cdd5cb6&redirect_uri=http://p.jtanimation.com:8000/wxcode&response_type=code&scope=snsapi_base&agentid=1000013&state=STATE#wechat_redirect'
    print(url)
    return redirect(url)

def wxcode(request):
    if request.method  == "GET":
        if 'code' in request.GET:
            code = request.GET["code"]

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

            print(url)

            r = requests.get(url, params=v)
            t = json.loads(r.text)

            print(t)

            seluser = t['UserId']
            users = hr_hr.objects.filter(userid=seluser)
            if users:
                u = users.first()
                rnd = seluser + str(time.time()) + str(random.randint(10000, 20000))
                strsession = hashlib.md5()
                strsession.update(rnd.encode('utf-8'))
                s = strsession.hexdigest()
                u.session = s
                u.save()

                gourl = redirect('/')
                gourl.set_cookie('usercookie', s, 14400)
                return gourl

    return HttpResponse('wxcode')

def wxtext(request):
    return HttpResponse('xtT9JTstqSGD5Lu2')

def property_list(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='property_list'

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

    # print("%s\n%s" % (request.method,request.GET))
    if request.method == "POST":
        print(request.POST)
        if "act" in request.POST:
            if request.POST['act'] == 'sort':
                sns = request.POST['Field']
                ps = asset_property.objects.filter(active=True).values('id',
                                                         'status',
                                                         'sid',
                                                         'name',
                                                         'specifications',
                                                         'purchase',
                                                         'warranty',
                                                         'user__name',
                                                         'user__active',
                                                         'position',
                                                         'sn').order_by(sns)

                s=[]
                u=list(ps)
                for t in u:
                    if t['purchase']:
                        t['purchase']=t['purchase'].strftime("%Y-%m-%d")
                    if t['warranty']:
                        t['warranty']=t['warranty'].strftime("%Y-%m-%d")
                    s.append(t)
                data=json.dumps(s)
                return HttpResponse(data,content_type="application/json")
            if request.POST['act'] == 'filter':
                pass
    else:
        ps = asset_property.objects.filter(active=True).values('id',
                                                         'status',
                                                         'sid',
                                                         'name',
                                                         'specifications',
                                                         'purchase',
                                                         'warranty',
                                                         'user__name',
                                                         'user__active',
                                                         'position',
                                                         'sn').order_by('name','specifications', 'sid')

        context['context'] = ps

    return render(request, 'property_list.html', context)

def property_form(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='设备单'

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

                # 当前设备id、前后id
                pn = int(request.GET['id'])
                ppn = pn-1
                npn = pn+1
                context['pk'] = pn
                context['ppk'] = ppn
                context['npk'] = npn

                #设备总数
                spn = asset_property.objects.filter(active=True).count()
                context['spk'] = spn

                # 设备类型DisplayName计算
                cats = asset_category.objects.filter(active=True).order_by('parentid','name')
                lcats = []
                for cat in cats:
                    ncat = {}
                    ncat["id"] = cat.id
                    ncat["name"] = cat.name
                    ncat["displayname"] =partt(cat.id)
                    lcats.append(ncat)
                context['cats'] = lcats

                # 可用人员查询
                hrs = hr_hr.objects.filter(active=True).order_by('name')
                context['hrs']= hrs

                try:
                    # 当前设备信息
                    ps = asset_property.objects.get(id=pn)
                except Exception:
                    return redirect('/property_list/')
                else:
                    print(ps.purchase)
                    print(type(ps.purchase))
                    context['context'] = ps

                    # 设备配件获取
                    prs = ps.asset_parts_set.all()
                    context['parts'] = prs
                    context['partsnum'] = prs.count()

                # 设备照片信息
                asspic = asset_attachment.objects.filter(property=pn,active=True, final=True).first()
                if asspic:
                    context['imgid'] = asspic.id
                    context['headimg'] = asspic.filepath
                else:
                    # 如果无图则传占位符
                    context['imgid'] = 0
                    context['headimg'] = 'holder.js/100x100'
            elif request.GET['act'] == "disheadimg":
                pn = int(request.GET['id'])
                ps = asset_attachment.objects.filter(property=pn, active=True).values("id","name","filepath")

                # 返回JSON数据格式 0:为正常
                # {"code": 0, "msg": "OK", "data": [1,2,3,]}
                msg = {}
                msg['code'] = 0
                msg['msg'] = "OK"

                # 附加数据
                ldata = list(ps)
                msg['data'] = ldata
                data = json.dumps(msg)

                return HttpResponse(data, content_type="application/json")
            elif request.GET['act'] == "chacksid":
                val = request.GET['sid']
                t = asset_property.objects.filter(sid=val).first()
                data = {}
                if t:
                    data['code'] = 1
                    data['msg'] = "fail"
                    data['data'] = "输入值已存在"
                else:
                    data['code'] = 0
                    data['msg'] = "OK"
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            elif request.GET['act'] == "chacksn":
                val = request.GET['sn']
                t = asset_property.objects.filter(sn=val).first()
                data = {}
                if t:
                    data['code'] = 1
                    data['msg'] = "fail"
                    data['data'] = "输入值已存在"
                else:
                    data['code'] = 0
                    data['msg'] = "OK"
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            elif request.GET['act'] == "create":
                context['act'] = "create"
                context['pk'] = 0

                # 新建设置默认值
                cats = asset_category.objects.filter(active=True).order_by('parentid','name')
                lcats = []
                for cat in cats:
                    ncat = {}
                    ncat["id"] = cat.id
                    ncat["name"] = cat.name
                    ncat["displayname"] =partt(cat.id)
                    lcats.append(ncat)
                context['cats'] = lcats

                hrs = hr_hr.objects.filter(active=True).order_by('name')
                context['hrs']= hrs

                ps={}
                # 默认编号
                # Todo 这编号在建立规则后，可以根据规则生成
                # ps['sid'] = 0

                # 默认价格
                ps["price"] = 0

                # 默认出厂、维保、报废日期
                t =datetime.datetime.now()
                ps["manufacture"] = ps["purchase"] = ps["warranty"] = t
                context['context'] = ps

                return render(request, 'property_form.html', context)
            elif request.GET['act'] == "edit":
                pass

    elif request.method == "POST":
        print(request.POST)
        if "act" in request.POST:
            if request.POST['act'] == "active":
                assid = int(request.POST['id'])
                act = asset_property.objects.filter(id=assid).update(active=True)
                return HttpResponse(act)
            if request.POST['act'] == 'unactive':
                assid = int(request.POST['id'])
                act = asset_property.objects.filter(id=assid).update(active=False)
                return HttpResponse(act)
            if request.POST['act'] == 'delimg':
                id = int(request.POST['id'])
                a = asset_attachment.objects.filter(id=id).update(active=False,final=False)
                pid = int(request.POST['pid'])

                n = asset_attachment.objects.filter(property=pid,active=True).order_by('-id').first()
                data = {}
                # 返回1.失败1 2.成功：无图2、有图0
                if n:
                    n.final = True
                    n.save()
                    data['code'] = 0
                    data['msg'] = "OK"
                    data['id'] = n.id
                    data['filepath'] = n.filepath
                else:
                    data['code'] = 2
                    data['msg'] = "OK"
                    data['id'] = 0

                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            if request.POST['act'] == 'create':
                act='create'

                ugcatid = int(request.POST['categoryid'])
                if ugcatid == 0:
                    catid = None
                else:
                    catid = asset_category.objects.filter(id=ugcatid).first()

                guserid = int(request.POST['user'])
                if guserid == 0:
                    userid = None
                else:
                    userid = hr_hr.objects.filter(id=guserid).first()

                # 获取默认日期，当天日期
                pdate = request.POST['purchase']
                if pdate == '':
                    purchase = datetime.datetime.today()
                else:
                    purchase = datetime.datetime.strptime(pdate, "%Y-%m-%d")

                wdat = request.POST['warranty']
                if wdat == '':
                    warranty = datetime.datetime.today()
                else:
                    warranty = datetime.datetime.strptime(wdat, "%Y-%m-%d")

                rdat = request.POST['manufacture']
                if rdat == '':
                    manufacture = datetime.datetime.today()
                else:
                    manufacture = datetime.datetime.strptime(rdat, "%Y-%m-%d")

                item = asset_property(
                    sid = request.POST['sid'],
                    name = request.POST['name'],
                    sn=request.POST['sn'],
                    specifications = request.POST['specifications'],
                    model = request.POST['model'],
                    categoryid = catid,
                    purchase = purchase,
                    price = int(request.POST['price']),
                    manufacture = manufacture,
                    warranty = warranty,
                    user = userid,
                    # partlist = request.POST[''],
                    position = request.POST['position'],
                    status = 1,
                    nots = request.POST['comment'],
                    active = True
                )

                item.save()
                id = item.id
                return HttpResponse(id)
            if request.POST['act'] == 'edit':
                act='edit'
                id = int(request.POST['id'])
                return HttpResponse(id)

    return render(request, 'property_form.html', context)

def property_upload(request):
    print(request.POST)
    if request.method == "POST":
        f = request.FILES["file"]
        filePath = os.path.join(settings.MDEIA_ROOT, 'property\img', f.name)
        print(filePath)
        with open(filePath,'wb') as fp:
            for info in f.chunks():
                fp.write(info)

        pid = int(request.POST['id'])
        try:
            propertyid = asset_property.objects.get(id=pid)
        except Exception:
            return HttpResponse('data no')

        asset_attachment.objects.filter(property=pid).update(final=False)

        pth='/static/upfile/property/img/' + f.name
        k = asset_attachment(property=propertyid,
                             name=f.name,
                             filepath=pth,
                             oldname=f.name,
                             version=0,
                             final=True,
                             category='0')
        k.save()
        data= {}
        data['id'] = k.id
        data['filepath'] = k.filepath

        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponse('no')

def parts_list(request):
    context={}
    context['title']='parts_list'

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

    ps = asset_parts.objects.all().order_by('name')
    context['context'] = ps

    return render(request, 'parts_list.html', context)

#功能测试路由
def importdata(request):
    wb = load_workbook("kkk.xlsx")

    # # 导入设备
    # sheet = wb.get_sheet_by_name("Sheet2")
    # print(sheet["C1"].value)
    #
    # p = list()
    # x = 0
    # for i in sheet["A"]:
    #     x += 1
    #     if x != 1:
    #         u = sheet["F"+str(x)].value
    #         m = sheet["I"+str(x)].value
    #         w = sheet["J"+str(x)].value
    #         p.append(asset_property(
    #             sid=sheet["B"+str(x)].value,
    #             name=sheet["C"+str(x)].value,
    #             specifications=sheet["E"+str(x)].value,
    #             model=sheet["T"+str(x)].value,
    #             # categoryid=sheet["E"+str(x)].value,
    #             purchase=u.date(),
    #             price=sheet["N"+str(x)].value,
    #             manufacture=m.date(),
    #             warranty=w.date(),
    #             sn=sheet["H"+str(x)].value,
    #             # user=sheet["Q"+str(x)].value,
    #             partlist=1,
    #         ))
    # # asset_property.objects.bulk_create(p)


    # # 导入设备使用人
    # x = 0
    # m = 0
    # n = 0
    # w = 0
    # for i in sheet["A"]:
    #     x += 1
    #     if x != 1:
    #         s = sheet["B" + str(x)].value
    #         c =sheet["Q"+str(x)].value
    #
    #         cou = hr_hr.objects.filter(name=c).first()
    #         if c:
    #             if cou:
    #                 w += 1
    #                 # asset_property.objects.filter(sid=s).update(user=cou)
    #             else:
    #                 m += 1
    #         else:
    #             n += 1
    # print("空=%s   无=%s   写=%s"% (n,m,w))

    # # 导入类型
    # sheet1 = wb["Sheet1"]
    # n = 0
    # for i in sheet1['A']:
    #     n += 1
    #     if n != 1:
    #         namen = sheet1["B" + str(n)].value
    #         upd = sheet1["G" + str(n)].value
    #         upd = int(upd)+1
    #         up = sheet1["B" + str(upd)].value
    #         print("%s - %s" % (namen,up))
    #
    #         ni = asset_category.objects.filter(name=namen)
    #         if ni:
    #             puid = asset_category.objects.filter(name=up).first()
    #             asset_category.objects.filter(name=namen).update(parentid=puid)
    #         else:
    #             #add
    #             nn = asset_category(name=namen)
    #             nn.save()
    #             puid = asset_category.objects.filter(name=up).first()
    #             asset_category.objects.filter(name=namen).update(parentid=puid)

    # # 更新在用
    # it = asset_property.objects.filter(user__isnull=False).update(status=2)

    # # 导入类型
    # sheet1 = wb["Sheet2"]
    # n = 0
    # for i in sheet1['A']:
    #     n += 1
    #     if n != 1:
    #         ids = sheet1["B" + str(n)].value
    #         cat = sheet1["E" + str(n)].value
    #
    #         catn = asset_category.objects.filter(name=cat).first()
    #
    #         asset_property.objects.filter(sid=ids).update(categoryid=catn)
    #         print("%s - %s" % (ids,cat))

    # its = asset_property.objects.values_list('categoryid').annotate(Count('id'))
    # print(its.query)
    #
    # for it in its:.
    #     print(it)
    # print(type(it))

    # # 导入位置、使用状态
    # sheet1 = wb["Sheet2"]
    # n = 0
    # for i in sheet1['A']:
    #     n += 1
    #     if n != 1:
    #         ids = sheet1["B" + str(n)].value
    #         s = sheet1["Q" + str(n)].value
    #         p = sheet1["R" + str(n)].value
    #
    #         # sidn = asset_property.objects.filter(sid=ids).first()
    #
    #         asset_property.objects.filter(sid=ids).update(position=p,status=s)
    #         print("%s - %s-%s" % (ids,p,s))

    # if request.method == 'POST':
    #     print(request.POST)
    response = {"status":"ok"}
    return HttpResponse(response)

def search(request):
    context={}
    context['title']='pure list'

    # username = request.COOKIES.get('usercookie', None)
    # if username:
    #     try:
    #         signuser = hr_hr.objects.get(session=username)
    #     except Exception:
    #         context['userinfo'] = '用户'
    #         return render(request, 'sign.html', context)
    #     context['userinfo'] = signuser.name
    # else:
    #     context['userinfo'] = '用户'
    #     return render(request, 'sign.html', context)
    # print(signuser.id)

    # depid = 8
    # hre = hr_hr.objects.get(id=depid)
    # dpe = employee_department.objects.filter(employeeid__gender=1)
    # print(dpe.query)
    # print('--------------------------')
    # # print(dpe)
    # for i in dpe:
    #     print(i)
    #
    # print('=================================')
    # hre = employee_department.objects.all().values('employeeid__name','departmentid__name')
    # print(hre.query)
    # print('--------------------------')
    # print(hre)
    #
    # print('--------------------------')
    # hee = employee_department.objects.all()
    # for i in hee:
    #     print(i.employeeid.name)

    # em = hr_department.objects.get(pid=8)
    # print(em.employee_department_set.all())

    # h = hr_department.objects.get(pid=9)
    # lks = h.employee_department_set.all()
    # for p in lks:
    #     print(p.employeeid.name)

    # pr = asset_property.objects.get(pk=1)
    # pts = pr.asset_parts_set.all()
    # for pt in pts:
    #     print(pt.name)
    #
    # pr1 = asset_property.objects.filter(pk=1)
    # print(type(pr1), pr1.query)
    #
    # pr = asset_property.objects.get(pk=1)
    # print(type(pr))
    #
    # print(pr.name,
    #       pr.user.name,
    #       pr.user.employee_department_set.all().values('departmentid__name'))

    # q = asset_category.objects.all().values('name')
    # print(q)
    # for iq in q:
    #     print(iq)

    print(partt(4))
    return render(request, 'search.html',context)