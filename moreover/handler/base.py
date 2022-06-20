#! /usr/bin/env python
#
#
# @file: base
# @time: 2022/06/20
# @author: Mori
#


import traceback
from typing import Dict

from tornado.web import RequestHandler
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

        messages = "".join(lines)
        if len(messages):
            app_log.error(f"{status_code} with: {messages}")

        resp_json = render_json_resp(
            data={},
            code=500,
            traceback_payload=messages,
        )

        self.set_status(500)
        self.set_header(CONTENT_TYPE, JSON_MIME)
        self.write(resp_json)
        self.flush()
