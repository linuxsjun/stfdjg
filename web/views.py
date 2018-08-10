from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response

from web.models import pureftp
# Create your views here.

def index(request):
    context={}
    return render(request, 'base.html', context)

def hello(request):
    context={}
    context['hello']='this is .html! 页面'
    return render(request, 'hello.html', context)

def search_form(request):
    return render_to_response('search_form.html')

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
    response1=""

    list = pureftp.objects.all()
    # response2=Test.objects.filter(id=1)
    # response3=Test.objects.get(id=1)

    pureftp.objects.order_by("id")

    for var in list:
        response1 += "<p>" + var.user + " -> " + var.password + "</p> "
    response = response1
    return HttpResponse(response)