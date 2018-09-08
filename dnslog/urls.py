from django.conf.urls import url
from dnslog.views import *

urlpatterns = [
    url('^$', index, name='index'),
    url('getdata', getdata, name='getdata'),
    url('deldata', deledata, name='deldata'),
]
