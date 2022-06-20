#! /usr/bin/env python
#
#
# @file: form
# @time: 2022/06/20
# @author: Mori
#


from typing import Dict, Optional, Awaitable

from moreover.handler.base import ErrorTraceHandler


class FormHandler(ErrorTraceHandler):
    def prepare(self) -> Optional[Awaitable[None]]:
        self._form_data = None
        return super().prepare()

    @property
    def form_data(self) -> Dict:
        if self._form_data is None:
            self._form_data = {}
            for k, v in self.request.arguments.items():
                if not v:
                    self._form_data[k] = None
                else:
                    if len(v) == 1:
                        self._form_data[k] = v[0].decode("utf8")
                    else:
                        self._form_data[k] = [sub_v.decode("utf8") for sub_v in v]

            for k, v in self.request.files.items():
                self._form_data[k] = v[0]
        return self._form_data
