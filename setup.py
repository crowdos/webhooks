#!/usr/bin/python3

from distutils.core import setup

setup(name='webhooks tools',
      version='1.0',
      packages=['webhooks', 'webhooks.admin', 'webhooks.hooks', 'webhooks.obs'],
      scripts=['webhooks.py'],
      data_files=[('/etc/webhooks/', ['conf.json']),
                  ('/usr/share/webhooks', ['admin.wsgi', 'hooks.wsgi'])]
      )
