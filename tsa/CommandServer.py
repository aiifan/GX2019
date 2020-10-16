#!/usr/bin/python
# encoding=utf8

__author__ = 'LiRui'

import socket
import threading
import subprocess
import re


inet_pattern = re.compile(r'\s*inet addr:([\d\.]+)\s+(?:Bcast:[\d\.]+\s+)?Mask:([\d\.]+)')


def log(level, message):
    print '[{0}] {1}'.format(level, message)


INFO = 'INFO'
NOTICE = "NOTICE"
WARN = 'WARN'
ERROR = 'ERROR'

def receive_all(s):
    data = ''
    try:
        d = s.recv(1024)
        while d:
            data += d
            d = s.recv(1024)
    finally:
        return data


def send_all(s, data):
    while data:
        length = s.send(data)
        if not length:
            break
        data = data[length:]


def execute(command):
    log(INFO, 'execute command: ' + command)
    return _execute(command)


def _execute(command):
    commands = command.split()
    print commands
    return str(subprocess.Popen(commands, stdout=subprocess.PIPE).communicate()[0])


def query_ip(nicName):
    log(INFO, 'query ip of ' + nicName)
    ifconfig = _execute('ifconfig ' + nicName)
    for line in ifconfig.split('\n'):
        m = inet_pattern.match(line)
        if m:
            return m.group(1) + '|' + m.group(2)
    return ''


def query_route():
    log(INFO, 'query route')
    route = _execute('route')
    entries = []
    for line in route.split('\n')[2:]:
        line = line.strip()
        if not line: continue
        destination, gateway, mask = line.split()[0:3]
        if gateway == '*':
            continue
        elif destination == 'default':
            entries.append('default| | |' + gateway)
        else:
            entries.append('net|' + destination + '|' + mask + '|' + gateway)
    return '\n'.join(entries)


def serve(s):
    try:
        command = receive_all(s)
        if command:
            t, d = command.split(':', 2)
            t = t.strip()
            if t == 'command':
                result = execute(d.strip())
            if t == 'query_ip':
                result = query_ip(d.strip())
            if t == 'query_route':
                result = query_route()
            if result:
                send_all(s, result)
                s.shutdown(socket.SHUT_WR)
    finally:
        s.close()


def daemonize(pid_file, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    import sys, os, time, atexit
    from signal import SIGTERM
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, ex:
        sys.stderr.write('fork #1 failed: {0}({1})\n'.format(e.errno, e.strerror))
        sys.exit(1)

    os.setsid()
    os.chdir('/')
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, ex:
        sys.stderr.write('fork #2 failed: {0}({1})\n'.format(e.errno, e.strerror))
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno());
    os.dup2(so.fileno(), sys.stdout.fileno());
    os.dup2(se.fileno(), sys.stderr.fileno());

    def delete_pid():
        os.remove(pid_file)

    atexit.register(delete_pid)
    pid = str(os.getpid())
    open(pid_file, 'w+').write('{0}\n'.format(pid))

def main():
    server_socket = socket.socket()
    server_socket.bind(('127.0.0.1', 1700))
    server_socket.listen(5)

    while True:
        s, address = server_socket.accept()
        log(INFO, 'new connection: {0}'.format(address))
        threading.Thread(target=serve, args=(s, )).start()


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1 or sys.argv[1] != 'normal': 
        daemonize('/var/run/CommandServer.pid', stdout='/var/log/CommandServer.normal.log', stderr='/var/log/CommandServer.error.log')
    main()
