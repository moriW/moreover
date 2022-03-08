#! /bin/python
# json handler
#
# @file: json
# @time: 2022/02/03
# @author: Mori
#

import traceback
from typing import Dict, List, Union, Optional, Awaitable

from tornado.log import app_log
from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_decode, json_encode

from moreover.base.config import global_config, define

JSON_MIME = "application/json"
CONTENT_TYPE = "Content-Type"

define("ENABLE_TRACEBACK", default_value=True)


class JsonRequestHandler(RequestHandler):
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
                        self._query_data[k] = [
                            sub_v.decode('utf8')
                            for sub_v in v
                        ]
        return self._query_data

    def prepare(self) -> Optional[Awaitable[None]]:
        self._body_data = None
        self._query_data = None
        return super().prepare()


class JsonResponseHandler(RequestHandler):
    def render_json(
        self,
        data: Union[Dict, List] = {},
        code: int = None,
        message: str = None,
        traceback_payload: List[str] = [],
    ):
        payload = {
            "data": data,
            "error": {"code": code, "message": message, "traceback": []},
        }

        if traceback_payload is not None and len(traceback_payload) > 0:
            payload["error"]["traceback"] = traceback_payload

        self.write(json_encode(payload))
        if code is not None and code > 500:
            self.set_status(400)
        self.set_header(CONTENT_TYPE, JSON_MIME)
        return self.flush()

    def write_error(self, status_code: int, **kwargs: Dict) -> None:
        lines = []
        if global_config.ENABLE_TRACEBACK and global_config.DEBUG:
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
        if len(lines):
            app_log.error(f"{status_code} with: {''.join(lines)}")
        self.render_json(
            {},
            code=status_code,
            message=self._reason,
            traceback_payload=lines,
        )


class JsonHandler(JsonRequestHandler, JsonResponseHandler):
    ...
