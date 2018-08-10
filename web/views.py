from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response

from web.models import Test
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

    if 'name' in request.GET:
        test = Test(name=request.GET['name'])
        test = Test(crnu=request.GET['crnu'])
        test.save()
        print("int -> %s"%test.name)
        message['message'] = 'Null->' + test.name + ' ok'
    else:
        message['message']= 'Null'

    return render(request, 'search.html',message)

def data(request):
    test= Test(name='runoob')

    test.save()
    print(request)

    message='{% extends "base.html" %}{% block mainbody %}<p>ok</p>{% endblock %}'
    return HttpResponse(message)

def getdata(request):
    response=""
    response1=""

    list = Test.objects.all()
    # response2=Test.objects.filter(id=1)
    # response3=Test.objects.get(id=1)

    Test.objects.order_by("id")

    for var in list:
        response1 += "<p>" + var.name + " -> " + str(var.crnu) + "</p> "
    response = response1
    return HttpResponse(response)