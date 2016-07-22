#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import flask
import json
import ipaddress
import requests
from admin import db

class App:
    def __init__(self, conf, host='localhost', port=5000, debug=False):
        self.conf = conf
        self.app = flask.Flask(__name__)
        self.app.debug = debug
        self.host = host
        self.port = port

        self.app.add_url_rule('/', 'index', self.index, methods=['POST'])

    def index(self):
        if not self.__verify_remote_address():
            flask.abort(403)

        # TODO: verify secret

        # support ping:
        if self.__event_is_ping():
            return self.__pong()

        data = flask.request.json

        # Now react:

    def __event_is_ping(self):
        event = flask.request.headers.get('X-GitHub-Event')
        return event == 'ping'

    def __pong(self):
        return json.dumps({'msg': 'pong'})

    def __verify_remote_address(self):
        if not self.conf['github']['github_ips_only']:
            return True

        remote_addr = ipaddress.ip_address(flask.request.remote_addr)
        r = requests.get('https://api.github.com/meta')

        try:
            for ip in r.json()['hooks']:
                if remote_addr in ipaddress.ip_network(ip):
                    return True
        except:
            return False

        return False

    def run(self):
        self.app.run(host=self.host, port=self.port)
