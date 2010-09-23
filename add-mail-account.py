#!/usr/bin/python
# -*- coding: utf-8 -*-

import commands
import sys

DOVECOTPW = '/usr/sbin/dovecotpw'
UID = 6000
GID = 6000
PWD_FILE = "/etc/dovecot.pwd"
MAIL_BOX_FILE = "/etc/postfix/vmailbox"
POSTMAP = '/usr/sbin/postmap'
SERVICE = '/sbin/service'

def syori1(mailaddress, password):

    print 'dovecot パスワードを用意します。'
    for line in open(PWD_FILE):
        if line.startswith(mailaddress):
            error_message = 'メール アドレス (%s) はすでにファイル (%s) に存在します。' % (mailaddress, PWD_FILE)
            sys.exit(error_message)

    cmdline = '%s -s CRAM-MD5 -p %s' % (DOVECOTPW, password)
    ret = commands.getstatusoutput(cmdline)
    if ret[0] != 0:
        sys.exit(ret[1])
    insert_line = mailaddress + ':' + ret[1] + ':' + str(UID) + ':' + str(GID) + '::\n'
    f = open(PWD_FILE, 'a')
    f.write(insert_line)
    f.close()

def syori2(mailaddress):

    print 'postfix にメール ボックスを用意します。'
    for line in open(MAIL_BOX_FILE):
        if line.startswith(mailaddress):
            error_message = 'メール アドレス (%s) はすでにファイル (%s) に存在します。' % (mailaddress, MAIL_BOX_FILE)
            sys.exit(error_message)
            
    list = mailaddress.split('@')
    insert_line = mailaddress + ' ' + list[1] + '/' + list[0] + '/\n'
    f = open(MAIL_BOX_FILE, 'a')
    f.write(insert_line)
    f.close()

    print 'postmap します。'
    cmdline = POSTMAP + ' ' + MAIL_BOX_FILE
    ret = commands.getstatusoutput(cmdline)
    if ret[0] != 0:
        sys.exit(ret[1])

def restart(service_name):

    print '再起動 (%s) します。' % service_name
    cmdline = SERVICE + ' ' + service_name + ' restart'
    ret = commands.getstatusoutput(cmdline)
    if ret[0] != 0:
        sys.exit(ret[1])

def print_usage():
    print "usage: " + sys.argv[0] + " <mailaddress> <password>"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(2)
    else:
        syori1(sys.argv[1], sys.argv[2])
        syori2(sys.argv[1])
        restart('dovecot')
        restart('postfix')
        sys.exit(0)



