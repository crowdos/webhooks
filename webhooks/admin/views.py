#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import flask
import flask_admin.contrib.sqla
from webhooks import obs

class View(flask_admin.contrib.sqla.ModelView):
    form_base_class = flask_admin.form.SecureForm
    column_display_pk = True
    column_hide_backrefs = False
    column_labels = dict(url='URL', id='ID',
                         repo_r='Repository', project_r='Project', package_r='Package',
                         hook_r='Hook', sha1='SHA1', timestamp='Time')
    column_default_sort = 'id'
    page_size = 50

class HookView(View):
    column_list = ['id', 'project_r', 'package_r', 'repo_r', 'branch', 'enabled']
    can_view_details = True
    details_modal = True
    column_details_list = ['project_r', 'package_r', 'repo_r', 'branch',
                           'timestamp', 'tag', 'sha1', 'enabled']
    column_formatters = dict(timestamp=lambda v, c, m, p: (m.data and time.ctime(m.data.timestamp)) or '-',
                             sha1=lambda v, c, m, p: (m.data and m.data.sha1) or '-',
                             tag=lambda v, c, m, p: (m.data and m.data.tag) or '-')
    column_filters = ['branch', 'project_r', 'package_r', 'repo_r', 'enabled']
    form_columns = ['project_r', 'package_r', 'repo_r', 'branch', 'enabled']

class HookDataView(View):
    column_default_sort = ('timestamp', True)
    column_list = ['id', 'timestamp', 'tag', 'sha1', 'repo', 'project', 'package']
    column_formatters = dict(timestamp=lambda v, c, m, p: time.ctime(m.timestamp),
                             repo=lambda v, c, m, p: m.hook_r.repo_r.url,
                             project=lambda v, c, m, p: m.hook_r.project_r.name,
                             package=lambda v, c, m, p: m.hook_r.package_r.name)

    # We use a lambda so we can return the current epoch at the time of form generation
    form_args = dict(timestamp=dict(default=lambda: int(time.time())))

    @flask_admin.actions.action('trigger', 'Trigger', 'Trigger hook?')
    def action_trigger(self, ids):
        for id in ids:
            hook_data = self.get_one(id)
            hook = hook_data.hook_r
            s = str(hook_data)
            client = obs.Client(View.conf)
            package = obs.Package(client, name=hook.package_r.name, project=hook.project_r.name)
            if not package.ensure():
                flask.flash('Failed to create package for %s.' % (s), 'error')
            elif not package.update_service(url=hook.repo_r.url, branch=hook.branch, revision=hook_data.tag):
                flask.flash('Failed to trigger service for %s.' % (s), 'error')
            else:
                flask.flash('Successfully triggered %s.' % (s), 'success')
                hook_data.update_timestamp()
                self.session.commit()
