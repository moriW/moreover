#! /bin/python
# json handler
#
# @file: json
# @time: 2022/02/03
# @author: Mori
#

from typing import Dict, List, Union, Optional, Awaitable

from tornado.web import HTTPError
from tornado.escape import json_decode
from moreover.handler.base import ErrorTraceHandler


from moreover.handler.utils import render_json_resp, CONTENT_TYPE, JSON_MIME


__all__ = ["JsonRequestHandler", "JsonResponseHandler", "JsonHandler"]


class JsonRequestHandler(ErrorTraceHandler):
    @property
    def body_data(self) -> Union[Dict, List]:
        if self.request.method in ["POST", "PUT"] and self._body_data is None:
            if self.request.headers.get(CONTENT_TYPE, None) != JSON_MIME:
                raise HTTPError(
                    400, reason="ContentType not JSON or body not json type"
                )
            self._body_data = json_decode(self.request.body)
        return self._body_data or {}

    @property
    def query_data(self) -> Dict:
        if self._query_data is None:
            self._query_data = {}
            for k, v in self.request.query_arguments.items():
                if not v:
                    self._query_data[k] = None
                else:
                    if len(v) == 1:
                        self._query_data[k] = v[0].decode("utf8")
                    else:
                        self._query_data[k] = [sub_v.decode("utf8") for sub_v in v]
        return self._query_data

    def prepare(self) -> Optional[Awaitable[None]]:
        self._body_data = None
        self._query_data = None
        return super().prepare()


class JsonResponseHandler(ErrorTraceHandler):
    def render_json(
        self,
        data: Union[Dict, List] = {},
        code: int = None,
        message: str = None,
        traceback_payload: List[str] = [],
    ):
        json_resp = render_json_resp(
            data=data, code=code, message=message, traceback_payload=traceback_payload
        )
        self.write(json_resp)
        if code is not None and code > 1000:
            self.set_status(400)
        self.set_header(CONTENT_TYPE, JSON_MIME)
        return self.flush()


class JsonHandler(JsonRequestHandler, JsonResponseHandler):
    ...
