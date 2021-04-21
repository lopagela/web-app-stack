import logging
from wsgiref import simple_server

from api import app

logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)

log.debug("falcon API have been imported")

PORT = 8000
httpd = simple_server.make_server('127.0.0.1', PORT, app)
log.info(f"Start to serve the falcon server in development mode on {PORT=}")
httpd.serve_forever()
