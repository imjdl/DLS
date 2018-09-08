import sys
import os

import signal
from django.core.management.base import BaseCommand
from core.DNSDaemon import daemonize
from core.DNServer import dnsserver

PIDFILE = '/tmp/DNSserver.pid'


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            '--run',
            dest='run',
            help='run server[start|stop]',
        )

    def handle(self, *args, **options):

        try:
            if options['run'] == 'start':
                try:
                    daemonize(PIDFILE, stdout='/tmp/DNSserver.log', stderr='/tmp/DNSserver.log')
                except RuntimeError as e:
                    print(e, file=sys.stderr)
                    raise SystemExit(1)
                sys.stdout.write('DNSserver start with pid:{}'.format(os.getpid()))
                dnsserver()
            if options['run'] == 'stop':
                if os.path.exists(PIDFILE):
                    with open(PIDFILE) as f:
                        os.kill(int(f.read()), signal.SIGTERM)
                else:
                    print('Not running', file=sys.stderr)
                    raise SystemExit(1)
        except Exception as e:
            self.stdout.write(self.style.ERROR('命令出错'))
