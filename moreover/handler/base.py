#! /usr/bin/env python
#
#
# @file: base
# @time: 2022/06/20
# @author: Mori
#


import traceback
from typing import Dict

from tornado.web import RequestHandler, HTTPError
from tornado.log import app_log

from moreover.base.config import global_config, define
from moreover.handler.utils import render_json_resp, CONTENT_TYPE, JSON_MIME


define("ENABLE_TRACEBACK", default_value=True)


class ErrorTraceHandler(RequestHandler):
    def write_error(self, status_code: int, **kwargs: Dict) -> None:
        lines = []
        if global_config.ENABLE_TRACEBACK and global_config.DEBUG:
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)

        error = kwargs["exc_info"][1]
        tracebacks = "\n".join(lines)
        app_log.error(f"{status_code} with: {tracebacks}")

        resp = {
            "data": {},
            "code": status_code,
            "message": None,
            "traceback_payload": tracebacks,
        }
        if isinstance(error, HTTPError):
            self.set_status(400)
            resp["traceback_payload"] = []
            resp["message"] = error.log_message
        else:
            self.set_status(500)
            resp["message"] = None

        self.set_header(CONTENT_TYPE, JSON_MIME)
        self.write(render_json_resp(**resp))
        self.flush()
