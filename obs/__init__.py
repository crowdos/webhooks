#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import obs.templates

class Client:
    def __init__(self, conf):
        self.conf = conf

    def request(self, path, data=None):
        url = '%s/%s' % (self.conf['obs']['host'], '/'.join(path))
        if data:
            return requests.put(url,
                               auth=(self.conf['obs']['username'], self.conf['obs']['password']),
                               verify=self.conf['obs']['verify_ssl'], data=data)
        else:
            return requests.get(url,
                               auth=(self.conf['obs']['username'], self.conf['obs']['password']),
                               verify=self.conf['obs']['verify_ssl'])

class Project:
    def __init__(self, client, name=None):
        self.client = client
        self.name = name

    def ensure(self):
        if not self.exists():
            self.create()
        return self.exists()

    def exists(self):
        r = self.client.request(['source', self.name, '_meta'])
        return r.status_code == 200

    def create(self):
        data = obs.templates.NEW_PROJECT_TEMPLATE
        data = data.replace('@NAME@', self.name)
        r = self.client.request(['source', self.project, '_meta'], data)
        return self.exists()

class Package:
    def __init__(self, client, name=None, project=None):
        self.client = client
        self.name = name
        self.project = project

    def ensure(self):
        if not self.exists():
            self.create()
        return self.exists()

    def exists(self):
        r = self.client.request(['source', self.project, self.name, '_meta'])
        return r.status_code == 200

    def create(self):
        data = obs.templates.NEW_PACKAGE_TEMPLATE
        data = data.replace('@PACKAGE@', self.name).replace('@PROJECT@', self.project)
        r = self.client.request(['source', self.project, self.name, '_meta'], data)
        return self.exists()

    def update_service(self, url=None, branch=None, revision=None):
        data=obs.templates.SERVICE_TEMPLATE
        data = data.replace('@URL@', url).replace('@BRANCH@', branch).replace('@REVISION@', revision)
        r = self.client.request(['source', self.project, self.name, '_service'], data)
        return r.status_code == 200
