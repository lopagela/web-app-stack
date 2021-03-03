"""
Falcon API proxy server

Inspired from https://stackoverflow.com/a/55855266
"""
import os
import io
import logging
from typing import Optional

import falcon
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.debug("Logger configured")

hop_hop_headers = {
    'connection', 'keep-alive', 'proxy-authenticate',
    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
    'upgrade'
}

UPSTREAM = os.getenv("UPSTREAM", 'https://httpbin.org')


class Proxy:
    def __init__(self, upstream: str, prefix: Optional[str] = None):
        self.session = requests.Session()
        self.upstream = upstream
        if prefix:
            assert prefix.startswith("/") and not prefix.endswith("/")
        self._prefix = prefix
        self._prefix_len = 0 if not prefix else len(prefix)

    def handle(self, req: falcon.Request, resp: falcon.Response):
        target_url = self._build_target_url(req)
        client = req.access_route
        log.info(f"Proxying request for client={client} to path='{req.path}' and method='{req.method}' to target_path={target_url}")
        headers = dict(req.headers, Via='Falcon')
        # Skipping the content-length as it will fool the remote server
        for name in ('HOST', 'CONNECTION', 'REFERER', 'CONTENT-LENGTH'):
            headers.pop(name, None)
        log.debug(f"Preparing the request to url='{target_url}' with headers={headers}")
        request = requests.Request(method=req.method,
                                   url=target_url,
                                   data=req.bounded_stream.read(),
                                   headers=headers)
        prepared = request.prepare()
        log.debug(f"Request to url='{target_url}' has been prepared with headers={prepared.headers}")
        from_upstream = self.session.send(prepared, stream=True)
        log.debug(f"Streaming the response from url='{target_url}' method='{req.method}'")
        log.info(f"Got response for client={client} status_code={from_upstream.status_code} for method='{req.method}' on target_path='{target_url}'")
        received_headers = dict(from_upstream.headers.lower_items())
        # To avoid an assertion error raised by falcon when a load balancer is called
        for hop_hop in hop_hop_headers.intersection(received_headers.keys()):
            received_headers.pop(hop_hop)
        log.debug(f"Received the headers={received_headers}")
        resp.set_headers(received_headers)
        resp.content_type = from_upstream.headers.get('Content-Type', falcon.MEDIA_HTML)
        resp.status = falcon.get_http_status(from_upstream.status_code)
        resp.stream = from_upstream.iter_content(io.DEFAULT_BUFFER_SIZE)

    def _build_target_url(self, req):
        relative_path = req.path
        if self._prefix_len:
            relative_path = relative_path[self._prefix_len:]
        target_url = self.upstream + relative_path
        return target_url


api = falcon.API()
api.add_sink(sink=Proxy(upstream=UPSTREAM).handle, prefix=r"/")
api.add_sink(sink=Proxy(upstream="https://google.com", prefix="/google").handle, prefix="/google")
api.add_sink(sink=Proxy(upstream="https://httpbin.org/status", prefix="/test-status").handle, prefix="/test-status")

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
