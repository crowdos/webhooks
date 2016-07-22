#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
import flask_admin
import flask.ext.sqlalchemy

db = flask.ext.sqlalchemy.SQLAlchemy()

import app.models
import app.views

class App:
    def __init__(self, conf, host='localhost', port=5000, debug=False, echo=False):
        self.conf = conf

        self.app = flask.Flask(__name__)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.debug = debug
        self.app.config['SQLALCHEMY_ECHO'] = echo

        self.app.config['SECRET_KEY'] = conf['app']['secret_key']
        db_uri = 'mysql://%s:%s@%s/%s' % (conf['mysql']['username'], conf['mysql']['password'],
                                          conf['mysql']['host'], conf['mysql']['database'])
        self.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

        db.init_app(self.app)

        self.admin = flask_admin.Admin(self.app, template_mode='bootstrap3')

        self.host = host
        self.port = port

    def add_views(self):
        views.View.conf = self.conf
        self.admin.add_view(views.View(models.Repo, db.session))
        self.admin.add_view(views.View(models.Project, db.session))
        self.admin.add_view(views.View(models.Package, db.session))
        self.admin.add_view(views.HookView(models.Hook, db.session))
        self.admin.add_view(views.HookDataView(models.HookData, db.session))

    def run(self):
        self.app.run(host=self.host, port=self.port)
