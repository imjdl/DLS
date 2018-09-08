from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Log
# Create your views here.


def index(request):
    logdata = Log.objects.all()
    return render(request, 'dnslog/index.html', context={'logdata': logdata})


def getdata(request):
    logdata = Log.objects.all()
    res = []
    for log in logdata:
        data = {}
        data['IP'] = log.IP
        data['qtype'] = log.qtype
        data['text'] = log.text
        data['recvdate'] = log.recvdate
        res.append(data)
    return JsonResponse({'logdata': res})


def deledata(request):
    logdata = Log.objects.all()
    for i in logdata:
        i.delete()
    return HttpResponse(321)
