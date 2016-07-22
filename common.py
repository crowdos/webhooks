#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
import flask.ext.sqlalchemy
db = flask.ext.sqlalchemy.SQLAlchemy()

def create_app(conf, debug=None, echo=None):
    app = flask.Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.debug = debug
    app.config['SQLALCHEMY_ECHO'] = echo

    app.config['SECRET_KEY'] = conf['app']['secret_key']
    db_uri = 'mysql://%s:%s@%s/%s' % (conf['mysql']['username'], conf['mysql']['password'],
                                      conf['mysql']['host'], conf['mysql']['database'])
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    return app

class CommonApp(object):
    def __init__(self, conf, host='localhost', port=5000, debug=False, echo=False):
        self.conf = conf

        self.app = create_app(conf, debug, echo)

        self.host = host
        self.port = port

    def init(self):
        raise NotImplementedError()
