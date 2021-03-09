import logging
from typing import List

import falcon
from falcon.media.validators import jsonschema

# TODO make the log configuration outside this file to isolate the
#  API configuration and the technical configuration (log configuration)
logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)

schema_link_post_req = {
    "$schema": "https://json-schema.org/schema#",

    "type": "object",
    "properties": {
        "link": {"type": "string"},
    },
    "required": ["link"]
}

class Storage:
    MAP: List[str] = list()

    def get_all(self) -> List[str]:
        return self.MAP

    def put(self, value: str) -> bool:
        if not (value.startswith("http://") or value.startswith("https://")):
            log.warning(f"value='{value}' does not looks like a link, no storing it")
            return False
        if len(self.MAP) > 512:
            log.warning("The storage is already full of links, does not storing the value")
            return False
        if len(value) > 512:
            log.warning("Truncating link received in input")
            value = value[:512]
        self.MAP += [value]
        log.debug(f"One extra value stored, count={len(self.MAP)} values stored in total")
        return True


class LinkResource:
    storage = Storage()

    @jsonschema.validate(req_schema=schema_link_post_req)
    def on_post_link(self, req: falcon.Request, resp: falcon.Response) -> None:
        log.info(f"Received a request to save a link from sender={req.access_route}")
        link = req.media['link']
        is_saved = self.storage.put(link)
        resp.status = falcon.HTTP_OK
        resp.media = {"isSaved": is_saved, "link": link}

    def on_get_link(self, req: falcon.Request, resp: falcon.Response) -> None:
        log.info(f"Received a request to get links from sender={req.access_route}")
        resp.status = falcon.HTTP_OK
        resp.media = {"links": self.storage.get_all()}


def return_400(req: falcon.Request, resp: falcon.Response) -> None:
    log.debug(f"Received a request on path={req.path} with media={req.media}")
    resp.status = falcon.HTTP_OK
    resp.media = {"status": "success"}
    # raise falcon.HTTPBadRequest(title="Unknown endpoint",
    #                             description="Keep developing this application!")


class Server(falcon.App):

    def __init__(self):
        super(Server, self).__init__(middleware=falcon.CORSMiddleware())
        self.add_route("/api/v1/link", LinkResource(), suffix="link")
        self.add_sink(return_400)
        log.info("Server initialized")


api = Server()
