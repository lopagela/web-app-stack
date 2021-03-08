import logging
from wsgiref import simple_server

from backend.api import api

logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)

log.debug("falcon API have been imported")

httpd = simple_server.make_server('127.0.0.1', 8000, api)
log.info("Start to serve the falcon server in development mode")
httpd.serve_forever()
