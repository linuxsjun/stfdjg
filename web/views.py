from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests, time, datetime, pytz

from web.models import pureftp, base_conf
# Create your views here.

def index(request):
    context={}
    return render(request, 'base.html', context)

def hello(request):
    context={}
    context['hello']='this is .html! 页面'
    to='2018-08-11 18:52:56+00:00'
    # to='2018-08-11 18:52:56'
    # k = datetime.datetime.utcfromtimestamp()
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(time.time())))
    # print(time.strptime(to,"%Y-%m-%d %H:%M:%S"))
    # print(time.time())
    # print(time.mktime(time.gmtime(time.time())))
    # print(time.gmtime(time.time()))
    # print(time.gmtime(time.time()+7200))
    # print('----------------')
    # print(time.localtime(time.time()))
    # print(time.asctime(time.gmtime(time.time())))
    # print(time.mktime(time.strptime(time.asctime(time.gmtime(time.time())))))
    # print(time.timezone)
    return render(request, 'hello.html', context)

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

def getdata(request):
    response=""
    response1="l"

    list = pureftp.objects.all()
    # response2=Test.objects.filter(id=1)
    # response3=Test.objects.get(id=1)

    pureftp.objects.order_by("id")

    for var in list:
        response1 += "<p>" + var.user + " -> " + var.password + "</p> "
    response = response1
    return HttpResponse(response)