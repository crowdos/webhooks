#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import admin
import hooks
import json

def find_arg(name, default):
    try:
        i = sys.argv.index(name)
        return sys.argv[i+1]
    except:
        return default

def main():
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

    if '--admin' in sys.argv:
        app = admin.App(conf, host=host, port=port, debug=debug, echo=echo)
        app.add_views()
        app.run()
    elif '--hooks' in sys.argv:
        app = hooks.App(conf, host=host, port=port, debug=debug)
        app.run()
    else:
        sys.exit('An app must be chosen via --admin or --hooks')

if __name__ == '__main__':
    main()
