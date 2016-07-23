#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import flask
from webhooks import common
import github

class App(common.CommonApp):
    def init(self):
        self.app.add_url_rule('/', 'index', self.index, methods=['POST'])

    def index(self):
        if flask.request.headers.get('X-GitHub-Event'):
            return github.process(self.conf, flask.request)
        else:
            flask.abort(500, 'Unknown hook provider!')

    def run(self):
        self.app.run(host=self.host, port=self.port)
