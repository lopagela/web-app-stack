import logging

import falcon

log = logging.getLogger(__name__)


def return_400(req: falcon.Request, resp: falcon.Response) -> None:
    raise falcon.HTTPBadRequest(title="Unknown endpoint",
                                description="Keep developing this application!")


class Server(falcon.API):

    def __init__(self):
        super(Server, self).__init__()
        self.add_sink(return_400)
        log.info("Server initialized")


api = Server()
