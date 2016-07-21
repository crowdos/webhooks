#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
sys.path.append("flask-admin")

import time

from flask import Flask, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from flask_admin.form import SecureForm

app = Flask(__name__)
db = SQLAlchemy()

class Repo(db.Model):
    id = db.Column(mysql.INTEGER(10, unsigned=True), primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return self.url

class Project(db.Model):
    id = db.Column(mysql.INTEGER(10, unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return self.name

class Package(db.Model):
    id = db.Column(mysql.INTEGER(10, unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return self.name

class Hook(db.Model):
    id = db.Column(mysql.INTEGER(10, unsigned=True), primary_key=True, autoincrement=True)
    branch = db.Column(db.String(255), nullable=False)
    project = db.Column(mysql.INTEGER(10, unsigned=True),
                           db.ForeignKey('project.id', onupdate='CASCADE', ondelete='RESTRICT'),
                           nullable=False)
    package = db.Column(mysql.INTEGER(10, unsigned=True),
                           db.ForeignKey('package.id', onupdate='CASCADE', ondelete='RESTRICT'),
                           nullable=False)
    repo = db.Column(mysql.INTEGER(10, unsigned=True),
                        db.ForeignKey('repo.id', onupdate='CASCADE', ondelete='RESTRICT'),
                        nullable=False)
    project_r = db.relationship('Project', foreign_keys=project, lazy='select', uselist=False)
    package_r = db.relationship('Package', foreign_keys=package, lazy='select', uselist=False)
    repo_r = db.relationship('Repo', foreign_keys=repo, lazy='select', uselist=False)
    __table_args__ = (db.UniqueConstraint('project', 'package', 'branch', 'repo',
                                          name='table_index'), )

    def __repr__(self):
        return '%s [%s] %s %s' % (self.repo_r.url, self.branch, self.project_r.name, self.package_r.name)

class HookData(db.Model):
    id = db.Column(mysql.INTEGER(10, unsigned=True), primary_key=True, autoincrement=True)
    timestamp = db.Column(mysql.INTEGER(11, unsigned=True), nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    sha1 = db.Column(db.String(255), nullable=False)
    hook = db.Column(mysql.INTEGER(10, unsigned=True),
                     db.ForeignKey('hook.id', onupdate='CASCADE', ondelete='RESTRICT'),
                     nullable=False, unique=True)
    hook_r = db.relationship('Hook', foreign_keys=hook,
                             backref=db.backref('data', lazy='select', uselist=False))

    def __repr__(self):
        return '%s [%s] %s' % (self.sha1, self.tag, time.asctime(time.gmtime(self.timestamp)))

    def update_timestamp(self):
        self.timestamp = int(time.time())

class View(ModelView):
    form_base_class = SecureForm
    column_display_pk = True
    column_hide_backrefs = False
    column_labels = dict(url='URL', id='ID',
                         repo_r='Repository', project_r='Project', package_r='Package',
                         hook_r='Hook', sha1='SHA1', timestamp='Time')
    column_default_sort = 'id'
    page_size = 50

class HookView(View):
    column_list = ['id', 'project_r', 'package_r', 'repo_r', 'branch']
    can_view_details = True
    details_modal = True
    column_details_list = ['project_r', 'package_r', 'repo_r', 'branch', 'timestamp', 'tag', 'sha1']
    column_formatters = dict(timestamp=lambda v, c, m, p: time.ctime(m.data.timestamp),
                             sha1=lambda v, c, m, p: m.data.sha1,
                             tag=lambda v, c, m, p: m.data.tag)
    column_filters = ['branch', 'project_r', 'package_r', 'repo_r']
    form_columns = ['project_r', 'package_r', 'repo_r', 'branch']

class HookDataView(View):
    column_default_sort = ('timestamp', True)
    column_list = ['id', 'timestamp', 'tag', 'sha1', 'repo', 'project', 'package']
    column_formatters = dict(timestamp=lambda v, c, m, p: time.ctime(m.timestamp),
                             repo=lambda v, c, m, p: m.hook_r.repo_r.url,
                             project=lambda v, c, m, p: m.hook_r.project_r.name,
                             package=lambda v, c, m, p: m.hook_r.package_r.name)

    # We use a lambda so we can return the current epoch at the time of form generation
    form_args = dict(timestamp=dict(default=lambda: int(time.time())))

    @action('trigger', 'Trigger', 'Trigger hook?')
    def action_trigger(self, ids):
        for id in ids:
            d = self.get_one(id)
            d.update_timestamp()
            s = str(d)
            # TODO: implement me
            if False:
                flash('Successfully triggered %s.' % (s), 'success')
            else:
                flash('Failed to trigger %s.' % (s), 'error')

        self.session.commit()

# class IndexView(AdminIndexView):
#     column_descriptions = dict()
#     can_create = False
#     can_edit = False
#     can_delete = False

#     def is_editable(self, name):
#         return False

#     def is_sortable(self, name):
#         return False

#     def get_value(self, row, column):
#         pass
#     @expose('/')
#     def index(self):
#         data = dict(fpp='ssss')
#         count = 10
#         return self.render('admin/model/list.html', data=data,
#                            list_columns=[(id, 'ID')],
#                            count=count,
#                            page_size=count,
#                            num_pages=1,
#                            get_value=self.get_value)

def find_arg(name, default):
    try:
        i = sys.argv.index(name)
        return sys.argv[i+1]
    except:
        return default

if __name__ == '__main__':
    debug = False
    echo = False
    host = 'localhost'
    port = '5000'
    conf = None

    if '--debug' in sys.argv:
        debug = True
    if '--echo' in sys.argv:
        echo = True

    host = find_arg('--host', host)
    port = int(find_arg('--port', port))
    conf = find_arg('--conf', conf)

    if not conf:
        sys.exit("Configuration file must be supplied with --conf")

    conf = json.load(open(conf))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.debug = debug
    app.config['SQLALCHEMY_ECHO'] = echo

    app.config['SECRET_KEY'] = conf['app']['secret_key']
    db_uri = 'mysql://%s:%s@%s/%s' % (conf['mysql']['username'], conf['mysql']['password'],
                                      conf['mysql']['host'], conf['mysql']['database'])
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    admin = Admin(app, template_mode='bootstrap3')
#                  index_view=IndexView())
    db.init_app(app)

    admin.add_view(View(Repo, db.session))
    admin.add_view(View(Project, db.session))
    admin.add_view(View(Package, db.session))
    admin.add_view(HookView(Hook, db.session))
    admin.add_view(HookDataView(HookData, db.session))
#    admin.add_view(IndexView(IndexData, db.session))

    app.run(host=host, port=port)
