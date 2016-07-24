import sys
import json
from webhooks import admin, common

conf = json.load(open("/etc/webhooks/conf.json"))
app = admin.App(conf, debug=False, echo=False)
app.init()
application = app.app
