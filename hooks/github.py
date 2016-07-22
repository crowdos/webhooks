#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import ipaddress
import requests
import flask

def __verify_remote_address(conf, request):
    if not conf['github']['github_ips_only']:
        return True

    remote_addr = ipaddress.ip_address(request.remote_addr)
    r = requests.get('https://api.github.com/meta')

    try:
        for ip in r.json()['hooks']:
            if remote_addr in ipaddress.ip_network(ip):
                return True
    except:
        return False

    return False

def process(conf, request):
    if not __verify_remote_address(conf, request):
        flask.abort(403)

    # TODO: verify secret

    # support ping:
    if request.headers.get('X-GitHub-Event') == 'ping':
        return json.dumps({'msg': 'pong'})

    data = request.json
