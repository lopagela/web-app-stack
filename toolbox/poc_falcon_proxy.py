#!/usr/bin/env python3.9
import logging
from typing import Mapping
from urllib.parse import urljoin

import requests
import falcon

config: Mapping[str, str] = {
    "DST_PROXY": "https://dev.api.worldline.eu.jaris.io",
}

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
hop_hop_headers = {
    'connection', 'keep-alive', 'proxy-authenticate',
    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
    'upgrade'
}

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.debug("Logger configured")

api = falcon.API()


class RequestHandler:
    def __call__(self, req: falcon.Request, resp: falcon.Response) -> None:
        log.info(f"Processing an incoming requests='{req.method}', path='{req.path}'")
        target_url = urljoin(config["DST_PROXY"], req.path)
        log.debug(f"Proxying to url='{target_url}'")
        log.debug(f"Proxying with headers='{req.headers}'")
        response = requests.request(method=req.method, url=target_url, headers=req.headers)
        response_headers = dict(response.headers.lower_items())
        log.debug(f"Get headers={response_headers}")
        # TODO improve my perf
        for hop_hop in hop_hop_headers.intersection(response_headers.keys()):
            response_headers.pop(hop_hop)
        resp.status = falcon.get_http_status(response.status_code)
        resp.body = response.text
        resp.set_headers(response_headers)
        log.debug(f"Successfully made the proxy call for requests='{req.method}', path='{req.path}'")


api.add_sink(sink=RequestHandler(), prefix=r"/")

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
