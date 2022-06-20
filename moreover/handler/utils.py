#! /usr/bin/env python
#
#
# @file: utils
# @time: 2022/06/20
# @author: Mori
#


from typing import Union, Dict, List
from tornado.escape import json_encode


__all__ = ["JSON_MIME", "CONTENT_TYPE", "render_json_resp"]

JSON_MIME = "application/json"
CONTENT_TYPE = "Content-Type"


def render_json_resp(
    data: Union[Dict, List] = {},
    code: int = None,
    message: str = None,
    traceback_payload: List[str] = [],
) -> str:
    return json_encode(
        {
            "data": data,
            "error": {
                "code": code,
                "message": message,
                "traceback": traceback_payload or [],
            },
        }
    )
