#!/usr/bin/python
# -*- coding: utf-8 -*-

import hmac
import hashlib
import json
import ipaddress

__all__ = ['process']

def __verify_remote_address(conf, request):
    if not conf['github']['github_ips_only']:
        return True

    remote_addr = ipaddress.ip_address(request.remote_addr.decode())
    r = requests.get('https://api.github.com/meta')

    try:
        for ip in r.json()['hooks']:
            if remote_addr in ipaddress.ip_network(ip):
                return True
    except:
        return False

    return False

def __verify_signature(conf, request):
    key = conf['github']['enforce_secret']
    if not key:
        return True

    header = request.headers.get('X-Hub-Signature')
    if not header:
        return False

    if not header.startswith('sha1='):
        return False

    header = header[5:]
    mac = hmac.new(key.encode('utf8'), request.data, hashlib.sha1)

    return hmac.compare_digest(mac.hexdigest(), header.encode('utf-8'))

def process(conf, request):
    if not __verify_remote_address(conf, request):
        flask.abort(403)

    # Verify HMAC signature
    if not __verify_signature(conf, request):
        flask.abort(403)

    # support ping:
    if request.headers.get('X-GitHub-Event') == 'ping':
        return json.dumps({'msg': 'pong'})

    parser = PayloadParser(request.json)

    if not parser.is_created():
        return ''

    tag = parser.tag()
    if not tag:
        return 'Cannot find a tag'

    branch = parser.branch()
    if not branch:
        branch = 'master'

    repo = parser.repo()

    return {'branch': branch,
            'tag': tag,
            'sha1': parser.sha1(),
            'repo': repo,
            }

class PayloadParser:
    def __init__(self, o):
        self.o = o

    def is_created(self):
        try:
            forced = self.o['forced']
            created = self.o['created']
            return created == True or forced == True
        except:
            return False

    def repo(self):
        return self.o['repository']['ssh_url']

    def sha1(self):
        return self.o['after']

    def tag(self):
        return self.__parse(self.o['ref'], 'tags')

    def branch(self):
        return self.__parse(self.o['base_ref'], 'heads')

    def __parse(self, ref, token):
        try:
            ref = ref.split('/')
            if ref[0] != 'refs' or ref[1] != token:
                return None
            return ref[2]
        except:
            return None
