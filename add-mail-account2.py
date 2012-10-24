#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab softtabstop=4 number :

import commands
import sys

SASLPASSWD = '/usr/sbin/saslpasswd2'
POPAUTH = '/usr/sbin/popauth'
GROUPADD = '/usr/sbin/groupadd'
USERADD = '/usr/sbin/useradd'
MAP = '/usr/sbin/makemap'
TABLE = '/etc/mail/virtusertable'

def exec_cmd(cmd):
    ret = commands.getstatusoutput(cmd)
    if ret[0] != 0:
        sys.stderr.write('ERROR: ' + cmd)
        sys.exit(ret[1])

def add_group(user):
    print 'グループを追加'
    cmd = "%s '%s'" % (GROUPADD, user)
    exec_cmd(cmd)

def add_user(user, pwd):
    print 'ユーザーを追加'
    cmd = "%s --create-home -s /bin/false -g '%s' '%s'" % (USERADD, user, user)
    exec_cmd(cmd)

def add_sasl(user, pwd):
    print 'SASL を追加'
    cmd = "echo '%s' | %s '%s'" % (pwd, SASLPASSWD, user)
    exec_cmd(cmd)

def add_popauth(user, pwd):
    print 'popauth を追加'
    cmd = "%s -user '%s' '%s'" % (POPAUTH, user, pwd)
    exec_cmd(cmd)

def add_virtuser(domain, user):
    print 'virtuser を追加'
    cmd = "echo '%s@%s\t%s' >> %s" % (user, domain, user, TABLE)
    exec_cmd(cmd)
    cmd = "%s hash /etc/mail/virtusertable < /etc/mail/virtusertable" % (MAP)
    exec_cmd(cmd)

if __name__ == '__main__':
    domain = sys.argv[1]
    user = sys.argv[2]
    pwd = sys.argv[3]
    add_group(user)
    add_user(user, pwd)
    add_sasl(user, pwd)
    add_popauth(user, pwd)
    add_virtuser(domain, user)






