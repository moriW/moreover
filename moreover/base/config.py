#! /bin/python
# config store & parse
#
# @file: config
# @time: 2022/02/05
# @author: Mori
#

import json
from tornado.util import ObjectDict

from moreover.base.logger import gen_logger

global_config = ObjectDict()
logger = gen_logger("config")


def define(config: str, default_value: str):
    if config in global_config:
        logger.warning(f"key: {config} already exists")
        return
    global_config[config] = default_value


def parse_config_file(file: str):
    with open(file, "r") as _f:
        global_config.update(json.load(_f))
