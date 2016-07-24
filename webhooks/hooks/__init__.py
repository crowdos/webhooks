#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import flask
from webhooks import common, obs
import github
import flask
from webhooks.common import db
import webhooks.admin.models

class App(common.CommonApp):
    def init(self):
        self.app.add_url_rule('/', 'index', self.index, methods=['POST'])

    def index(self):
        data = None

        if flask.request.headers.get('X-GitHub-Event'):
            data = github.process(self.conf, flask.request)

        t = type(data)
        if t is int:
            flask.abort(data)
        elif t is str:
            return data
        elif not t is dict:
            flask.abort(500, 'Unknown parser return value!')

        if not self.__verify_data(data):
            flask.abort(500, 'Failed to parse payload!')

        output = self.__process_data(data)
        return '\n'.join(output)

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def __process_data(self, data):
        repo = webhooks.admin.models.Repo.query.filter_by(url=data['repo']).all()
        if not repo:
            return ['No repository found']
        repo = repo[0]

        # Now we need to find the hook:
        hooks = webhooks.admin.models.Hook.query.filter_by(repo=repo.id,
                                                           branch=data['branch']).all()
        if not hooks:
            return ['No configured hook']

        output = []
        client = obs.Client(self.conf)
        for hook in hooks:
            if not hook.data:
                hook.data = webhooks.admin.models.HookData()

            hook.data.update_timestamp()
            hook.data.tag = data['tag']
            hook.data.sha1 = data['sha1']

            if not hook.enabled:
                output.append('%s of %s is not enabled' % (hook.package_r.name, hook.project_r.name))
            else:
                # Now trigger the actual hook:
                package = obs.Package(client, project=hook.project_r.name,
                                      name=hook.package_r.name)
                if not package.ensure():
                    output.append('Cannot create %s of %s' % (package.name, package.project))
                elif not package.update_service(url=hook.repo_r.url, branch=branch, revision=tag):
                    output.append('Cannot trigger %s of %s' % (package.name, package.project))
                else:
                    output.append('Triggered %s of %s' % (package.name, package.project))

        db.session.commit()

        return output

    def __verify_data(self, data):
        if not data:
            return False

        keys = data.keys()

        for i in ['branch', 'tag', 'repo', 'sha1']:
            if not i in keys:
                return False

        return True
