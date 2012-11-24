#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab softtabstop=4 number :

import commands
import sys
import re

POSTMAP = '/usr/local/sbin/postmap'

DOMAIN = '/usr/local/etc/postfix/virtual_domains'
MAILBOX = '/usr/local/etc/postfix/vmailbox'
PASSWORD = '/usr/local/etc/dovecot/passwd'

def exec_cmd(cmd):
    ret = commands.getstatusoutput(cmd)
    if ret[0] != 0:
        sys.stderr.write('ERROR: ' + cmd)
        sys.exit(ret[1])

def postfix_add_domain(domain):
    print '--- postfix --- domain を追加'
    pattern = '^%s$' % domain
    for line in open(DOMAIN, 'r'):
        if re.match(pattern, line):
            print domain + " は既に存在する"
            return

    outfile = open(DOMAIN, 'a')
    outfile.write("%s\n" % domain)
    outfile.close()
    print '追加した'

def postfix_add_mainbox(domain, user):
    print '--- postfix --- mailbox を追加'
    mail_addr = user + '@' + domain
    pattern = '^%s ' % mail_addr
    for line in open(MAILBOX, 'r'):
        if re.match(pattern, line):
            print mail_addr + " は既に存在する"
            return

    outfile = open(MAILBOX, 'a')
    outfile.write("%s aiueo\n" % mail_addr)
    outfile.close()
    exec_cmd(POSTMAP + ' ' + MAILBOX)
    print '追加した'

def dovecot_add_password(domain, user, pwd):
    print '--- dovecot --- password を追加'
    mail_addr = user + '@' + domain
    pattern = '^%s:' % mail_addr
    for line in open(PASSWORD, 'r'):
        if re.match(pattern, line):
            print mail_addr + " は既に存在する"
            return

    outfile = open(PASSWORD, 'a')
    outfile.write("%s:{PLAIN}%s:virtual:virtual:(gecos):/home/virtual/%s/%s:(shell):\n" % (mail_addr, pwd, domain, user))
    outfile.close()
    print '追加した'

if __name__ == '__main__':
    domain = sys.argv[1]
    user = sys.argv[2]
    pwd = sys.argv[3]
    postfix_add_domain(domain)
    postfix_add_mainbox(domain, user)
    dovecot_add_password(domain, user, pwd)


