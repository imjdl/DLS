#!/usr/bin/env python3
# coding = UTF-8

import os
import sys

import atexit
import signal


def daemonize(pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):

    if os.path.exists(pidfile):
        raise RuntimeError('Aleady runing!!')

    # First fork
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('Fork #1 failed')
    os.chdir('/')
    os.setsid()
    os.umask(0)
    # second fork
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('Fork #2 failed')

    sys.stdout.flush()
    sys.stderr.flush()

    with open(stdin, 'rb') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab') as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # write PID file
    with open(pidfile, 'w') as f:
        print(os.getpid(), file=f)
    atexit.register(lambda: os.remove(pidfile))

    # Signal handler

    def signal_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, signal_handler)
