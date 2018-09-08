import socketserver

from django.conf import settings
from dnslib import *
from dnslog.models import Log
"""
以下的几种处理解析记录，
返回的均为假的数据。
DNSLog 目的是记录Log信息，
并不是真正又来做解析的。
"""

def dnsA(request):
    """
    处理A记录
    :param request:
    :return:
    """
    res = DNSRecord(DNSHeader(qr=1, aa=1, id=request.header.id), q=DNSQuestion(request.q.qname),
                    a=RR(request.q.qname, rdata=A("127.0.0.1"), ttl=3))
    return res

def dnsNS(request):
    """
    处理NS记录
    :param request:
    :return:
    """
    res = DNSRecord(DNSHeader(qr=1, aa=1, id=request.header.id), q=DNSQuestion(request.q.qname),
                    a=RR(request.q.qname, rdata=NS("ns0.flask.ga"), ttl=3))
    return res

def dnsMX(request):
    """
    处理MX记录
    :param request:
    :return:
    """
    res = DNSRecord(DNSHeader(qr=1, aa=1, id=request.header.id), q=DNSQuestion(request.q.qname),
                    a=RR(request.q.qname, rdata=MX("maill.flask,ga"), ttl=3))
    return res

def dnsCNAME(request):
    """
    处理MX记录
    :param request:
    :return:
    """
    res = DNSRecord(DNSHeader(qr=1, aa=1, id=request.header.id), q=DNSQuestion(request.q.qname),
                    a=RR(request.q.qname, rdata=CNAME('a.flask.ga'), ttl=3))
    return res


class DNSserver(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        try:
            request = DNSRecord.parse(data)
            res = self.dnsresponce(request)
            self.savelog(request)
            sock.sendto(bytes(res.pack()), self.client_address)
            self.savelog(request)
        except Exception:
            pass

    def dnsresponce(self, request):

        fun = {
            'A': dnsA,
            'NS': dnsNS,
            'MX': dnsMX,
            'CNAME': dnsCNAME,
        }

        # 根据查询的类型返回响应的数据
        qtype = QTYPE[request.q.qtype]
        return fun[qtype](request)

    def savelog(self, request):
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        l = Log(IP=self.client_address[0], qtype=qtype, text=qname)
        l.save()


def dnsserver():
    with socketserver.ForkingUDPServer((settings.DNSHOST, settings.DNSPORT), DNSserver) as s:
        s.serve_forever()


if __name__ == '__main__':

     with socketserver.ForkingUDPServer(('127.0.0.1', 10086), DNSserver) as s:
         s.serve_forever()
