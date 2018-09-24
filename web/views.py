from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import render_to_response
import requests, json, time, datetime, hashlib, random

import os
from django.conf import settings

from web.models import pureftp, base_conf, hr_department, hr_hr, employee_department, base_user_sign_log
from web.models import asset_conf, asset_category, asset_parts, asset_property, position

from openpyxl import load_workbook

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
            context['context'] = ps

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
        print(request)
        if "act" in request.POST:
            if request.POST['act'] == 'sort':
                sns = request.POST['Field']
                ps = asset_property.objects.all().values('id',
                                                         'status',
                                                         'sid',
                                                         'name',
                                                         'specifications',
                                                         'purchase',
                                                         'warranty',
                                                         'user__name',
                                                         'sn').order_by(sns)
                s=[]
                u=list(ps)
                for t in u:
                    t['purchase']=t['purchase'].strftime("%Y-%m-%d")
                    t['warranty']=t['warranty'].strftime("%Y-%m-%d")
                    s.append(t)
                data=json.dumps(s)
                return HttpResponse(data,content_type="application/json")
    else:
        ps = asset_property.objects.all().order_by('name','specifications', 'sid')
        context['context'] = ps

    return render(request, 'property_list.html', context)

def property_form(request):
    request.encoding = 'utf-8'
    context={}
    context['title']='property_form'

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
        if "act" in request.GET:
            print(request.GET)
            if request.GET['act'] == "display":
                pn = int(request.GET['id'])

                spn = asset_property.objects.filter(active=True).count()
                context['spk'] = spn

                cats = asset_category.objects.filter(active=True).order_by('name')
                context['cats'] = cats

                hrs = hr_hr.objects.filter(active=True).order_by('name')
                context['hrs']= hrs

                try:
                    ps = asset_property.objects.get(id=pn)
                except Exception:
                    return redirect('/property_list/')
                else:
                    context['pk']=pn
                    context['context'] = ps

                    prs = ps.asset_parts_set.all()
                    context['parts'] = prs

                # print(ps.categoryid.name)
    return render(request, 'property_form.html', context)

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
    # for it in its:
    #     print(it)
    # print(type(it))


    # if request.method == 'POST':
    #     print(request.POST)
    response = {"status":"ok"}
    return HttpResponse(response)

def search(request):
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
    print(signuser.id)

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

    pr = asset_property.objects.get(pk=1)
    pts = pr.asset_parts_set.all()
    for pt in pts:
        print(pt.name)

    pr1 = asset_property.objects.filter(pk=1)
    print(type(pr1), pr1.query)

    pr = asset_property.objects.get(pk=1)
    print(type(pr))

    print(pr.name,
          pr.user.name,
          pr.user.employee_department_set.all().values('departmentid__name'))



    return render(request, 'search.html',context)