#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import flask
import flask_admin.contrib.sqla

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

    @flask_admin.actions.action('trigger', 'Trigger', 'Trigger hook?')
    def action_trigger(self, ids):
        for id in ids:
            d = self.get_one(id)
            d.update_timestamp()
            s = str(d)
            # TODO: implement me
            if False:
                flask.flash('Successfully triggered %s.' % (s), 'success')
            else:
                flask.flash('Failed to trigger %s.' % (s), 'error')

        self.session.commit()
