import logging
from typing import List, Dict

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic.main import BaseModel


# TODO make the log configuration outside this file to isolate the
#  API configuration and the technical configuration (log configuration)

logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)

app = FastAPI()


class Link(BaseModel):
    url: str


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


storage = Storage()


@app.post("/api/v1/links")
def on_post_link(link: Link, request: Request) -> dict:
    log.info(f"Received a request to save a link from {request.client.host=}")
    is_saved = storage.put(link.url)
    return {"isSaved": is_saved, "url": link.url}


@app.get("/api/v1/links")
def on_get_link(request: Request) -> Dict[str, List[str]]:
    log.info(f"Received a request to get links from {request.client.host=}")
    return {"urls": storage.get_all()}


log.info("Server initialized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    log.info(f"{request.method=} on {request.url=} by {request.client.host=}")
    response: Response = await call_next(request)
    log.info(f"{response.status_code=} for {request.client.host=}")
    return response

log.info("CORS configured, accept everything")
