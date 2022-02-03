#! /bin/python
# json handler
#
# @file: json
# @time: 2022/02/03
# @author: Mori
#

# from urllib.error import HTTPError
import logging
import traceback
from typing import Dict, List, Union, Optional, Awaitable

from base.logger import gen_logger
from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode
from tornado.options import options

JSON_MIME = "application/json"
CONTENT_TYPE = "Content-Type"


class JsonHandler(RequestHandler):
    @property
    def data(self) -> Union[Dict, List]:
        return self._body_data or {}

    @property
    def logger(self) -> logging.Logger:
        if hasattr(self, "logger"):
            self.logger = gen_logger(self.__class__.__name__)
        return self.logger

    def prepare(self) -> Optional[Awaitable[None]]:
        self._body_data = None
        if self.request.method in ["POST", "PUT"]:
            assert self.request.headers[CONTENT_TYPE] == JSON_MIME
            self._body_data = json_decode(self.request.body)
        return super().prepare()

    def render_json(self, data: Union[Dict, List]):
        self.write(json_encode(data))
        self.set_header(CONTENT_TYPE, JSON_MIME)
        return self.flush()

    def write_error(self, status_code: int, **kwargs: Dict) -> None:
        self.set_header(CONTENT_TYPE, JSON_MIME)
        data = {}
        if options.ENABLE_TRACEBACK:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            data = {
                "error": {
                    "code": status_code,
                    "message": self._reason,
                    "traceback": lines,
                }
            }
            self.logger.error(f"{status_code} with: {lines}")
        else:
            data = {
                "error": {
                    "code": status_code,
                    "message": self._reason,
                }
            }
            self.logger.error(f"{status_code}")
        self.render_json(data)
