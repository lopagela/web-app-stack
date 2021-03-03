"""
Falcon API proxy server

Inspired from https://stackoverflow.com/a/55855266
"""
import io
import logging

import falcon
import requests

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.debug("Logger configured")

hop_hop_headers = {
    'connection', 'keep-alive', 'proxy-authenticate',
    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
    'upgrade'
}


class Proxy:
    UPSTREAM = 'https://httpbin.org'

    def __init__(self):
        self.session = requests.Session()

    def handle(self, req: falcon.Request, resp: falcon.Response):
        log.debug(f"Proxying request for path='{req.path}' and method='{req.method}'")
        headers = dict(req.headers, Via='Falcon')
        for name in ('HOST', 'CONNECTION', 'REFERER'):
            headers.pop(name, None)
        target_url = self.UPSTREAM + req.path
        log.debug(f"Preparing the request to url='{target_url}' with headers={headers}")
        request = requests.Request(method=req.method,
                                   url=target_url,
                                   data=req.bounded_stream.read(),
                                   headers=headers)
        prepared = request.prepare()
        from_upstream = self.session.send(prepared, stream=True)
        log.debug(f"Streaming the response from url='{target_url}' method='{req.method}'")
        received_headers = dict(from_upstream.headers.lower_items())
        for hop_hop in hop_hop_headers.intersection(received_headers.keys()):
            received_headers.pop(hop_hop)
        resp.set_headers(received_headers)
        resp.content_type = from_upstream.headers.get('Content-Type', falcon.MEDIA_HTML)
        resp.status = falcon.get_http_status(from_upstream.status_code)
        resp.stream = from_upstream.iter_content(io.DEFAULT_BUFFER_SIZE)


api = falcon.API()
api.add_sink(sink=Proxy().handle, prefix=r"/")

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
