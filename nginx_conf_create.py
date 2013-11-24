#!/usr/bin/env python
#coding=utf-8
#via: luwenju 2013/10/14 #

'''
    CLI Example::
        salt '*' nginx_config.output domain upstream_pool port ip,ip
'''

import sys
import commands
import httplib


def output (hostname, pool, port, ipadd):
    config = '''server {
      listen       80;
      server_name  %s;
      charset utf-8;
      location / {
              proxy_pass http://%s_pool;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $remote_addr;
              } 
              access_log /opt/log/nginx/%s_access.log main;
      }\n'''%(hostname, pool, hostname)

    f = open('/etc/nginx/conf.d/%s.conf' %hostname, 'w')
    f.write('%s' %config)
    f.close()

    ip_add= ipadd.split(',')
    f = open('/etc/nginx/conf.d/%s_upstream.conf' %hostname, 'w')
    f.write('upstream %s_pool {\n' %pool)
    for i in ip_add:
        f.write('    server %s:%s max_fails=2 fail_timeout=5s;\n' %(i, port))
    f.write('}\n')
    f.close()

    test_status = commands.getstatusoutput('service nginx configtest')[0]
    if test_status == 0:
        commands.getstatusoutput('service nginx reload')
        httpClient = httplib.HTTPConnection('ms.58control.cn', '80')
        httpClient.request('GET','/sms/warn?function=1000\&ms=nginx_reload_ok&mo=13520200311')
        httpClient.getresponse()
    else:
        httpClient = httplib.HTTPConnection('ms.58control.cn', '80')
        httpClient.request('GET','/sms/warn?function=1000\&ms=nginx_reload_error&mo=13520200311')
        httpClient.getresponse()
