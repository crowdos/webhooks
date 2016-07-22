#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from sqlalchemy.dialects import mysql
from app import db

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
