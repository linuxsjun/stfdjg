from django.shortcuts import render, redirect


from web.models import base_conf

# from hr.models import hr_department
from web.models import hr_department

from web.models import hr_hr, employee_department

import requests, json

# Create your views here.

def index(request):
    return redirect('/hr/hr/')

def hr_view(request):
    context = {}
    context['title'] = '人员'

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
    context['context'] = ps
    return render(request, 'view_hr_broad.html', context)

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
        print(t)
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