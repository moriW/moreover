#! /bin/python
# json handler
#
# @file: json
# @time: 2022/02/03
# @author: Mori
#

import logging
import traceback
from typing import Dict, List, Union, Optional, Awaitable

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_decode, json_encode

from moreover.base.logger import gen_logger
from moreover.base.config import global_config, define

JSON_MIME = "application/json"
CONTENT_TYPE = "Content-Type"

define("ENABLE_TRACEBACK", default_value=True)


class JsonHandler(RequestHandler):
    @property
    def data(self) -> Union[Dict, List]:
        if self.request.method in ["POST", "PUT"]:
            try:
                assert self.request.headers.get(CONTENT_TYPE, None) == JSON_MIME
                self._body_data = json_decode(self.request.body)
            except (AssertionError, Exception) as _:
                raise HTTPError(400, "ContentType not JSON or body not json type")
        return self._body_data or {}

    @property
    def logger(self) -> logging.Logger:
        return gen_logger(self.__class__.__name__)

    def prepare(self) -> Optional[Awaitable[None]]:
        self._body_data = None
        return super().prepare()

    def render_json(
        self,
        data: Union[Dict, List],
        code: int = None,
        message: str = None,
        traceback: List[str] = [],
    ):
        payload = {
            "data": data,
            "error": {
                "code": code,
                "message": message,
                "traceback": "\n".join(traceback),
            },
        }
        self.write(json_encode(payload))
        if code is not None and code > 500:
            self.set_status(400)
        self.set_header(CONTENT_TYPE, JSON_MIME)
        return self.flush()

    def write_error(self, status_code: int, **kwargs: Dict) -> None:
        lines = None
        if global_config.ENABLE_TRACEBACK and global_config.DEBUG:
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self.logger.error(f"{status_code} with: {lines}")
        self.render_json(
            {},
            code=status_code,
            message=self._reason,
            traceback=lines or [],
        )

