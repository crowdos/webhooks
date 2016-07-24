#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
import flask_admin
from webhooks import common
import views
import werkzeug
import pam

class App(common.CommonApp):
    def init(self):
        self.app.before_request(self.force_https)
        self.app.before_request(self.authenticate)

        self.admin = flask_admin.Admin(self.app, template_mode='bootstrap3')

        views.View.conf = self.conf

        self.admin.add_view(views.View(models.Repo, common.db.session))
        self.admin.add_view(views.View(models.Project, common.db.session))
        self.admin.add_view(views.View(models.Package, common.db.session))
        self.admin.add_view(views.HookView(models.Hook, common.db.session))
        self.admin.add_view(views.HookDataView(models.HookData, common.db.session))

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def force_https(self):
        if not flask.request.is_secure:
            # 301 is better but it causes the browser to always use https
            # which is a pain for testing
            url = flask.request.url.replace('http://', 'https://', 1)
            return flask.redirect(url, code=302)

    def is_authenticated(self):
        auth = flask.request.authorization
        if not auth or not 'username' in auth.keys() or not 'password' in auth.keys():
            return False

        p = pam.pam()
        return p.authenticate(auth['username'], auth['password'])

    # Idea from: https://blaxpirit.com/blog/14/hide-flask-admin-behind-simple-http-auth.html
    def authenticate(self):
        if not self.is_authenticated():
            raise werkzeug.exceptions.HTTPException('', flask.Response(
                "Please log in.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}))
