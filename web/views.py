from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests, json, time, datetime

from web.models import pureftp, base_conf, hr_department

# Create your views here.

def index(request):
    context={}
    return render(request, 'base.html', context)

def hr_view(request):
    context={}
    context['hello']='this is .html! 页面'

    # d = base_conf.objects.all().first()
    ps = hr_department.objects.all()

    context['context']= ''
    for p in ps:
        context['context']=context['context'] + "<tr>" + "<td>" + str(p.pid) + "</td><td></td><td></td><td></td>" + "</tr>"
        print(str(p.pid))

    return render(request, 'view_hr_list.html', context)

def search_form(request):
    return render_to_response('search_form.html')

def config(request):
    var = base_conf.objects.get(id=1)
    print(var.expirestime)
    # if var.token:
    #     nowtime=time.time()
    #     if time.mktime(time.strptime(var.expirestime)) > nowtime:
    #         print('token is ok')
    #     else:
    #         print('token is no')
    # else:
    #     print('token is no')

    if var.corpid :
        id=var.corpid
        secrect=var.corpsecret

    #todo 判断Token是否有效，如无效重新申请并存进数据库
    #todo Token 为空？
    #不为空在有效时间内？
    #有效用
    #无效：获取
    sendurl='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'%(id,secrect)

    r = requests.get(sendurl)

    print(r.content)

    context={}
    context['message']=r.content
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

    return render(request, 'search.html',message)

def data(request):
    test= pureftp(createdate='2019-9-9',
                  lastedate='2018-9-8',
                  user='test001')
    test.save()

    message='{% extends "base.html" %}{% block mainbody %}<p>ok</p>{% endblock %}'
    message='no'
    return HttpResponse(message)

def getToken(request):
    # response=""
    # response1=""
    #
    # list = pureftp.objects.all()
    # # response2=Test.objects.filter(id=1)
    # # response3=Test.objects.get(id=1)
    #
    # pureftp.objects.order_by("id")
    #
    # for var in list:
    #     response1 += "<p>" + var.user + " -> " + var.password + "</p> "
    # response = response1

    # d = base_conf.objects.all().first()
    d = base_conf.objects.get(pk=1)

    #https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRECT
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
        # print(time.asctime(time.localtime(tt)))
        # print(time.asctime(time.localtime(tt + t['expires_in'])))
        # print(time.asctime(time.gmtime(tt)))
        # print(time.asctime(time.gmtime(tt + t['expires_in'])))

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
    return redirect('/view/')