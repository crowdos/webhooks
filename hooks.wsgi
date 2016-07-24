import sys
import json
import logging
logging.basicConfig(stream=sys.stderr)

from webhooks import hooks, common

conf = json.load(open("/etc/webhooks/conf.json"))
app = hooks.App(conf, debug=False, echo=False)
app.init()
application = app.app
