#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
import flask_admin
import common
import admin.models
import admin.views

class App(common.CommonApp):
    def init(self):
        self.admin = flask_admin.Admin(self.app, template_mode='bootstrap3')

        views.View.conf = self.conf

        self.admin.add_view(views.View(models.Repo, common.db.session))
        self.admin.add_view(views.View(models.Project, common.db.session))
        self.admin.add_view(views.View(models.Package, common.db.session))
        self.admin.add_view(views.HookView(models.Hook, common.db.session))
        self.admin.add_view(views.HookDataView(models.HookData, common.db.session))

    def run(self):
        self.app.run(host=self.host, port=self.port)
