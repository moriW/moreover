#! /bin/python
# logger help
#
# @file: logger
# @time: 2022/02/01
# @author: Mori
#


import sys
import logging
from tornado.log import app_log, gen_log, access_log

loggers: dict = {}


def gen_logger(name: str) -> logging.Logger:
    if name not in loggers:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(
            logging.Formatter(
                "%(name)s@%(asctime)s-%(levelname)s: %(message)s", "%Y/%m/%d %H:%M:%S"
            )
        )
        logger.addHandler(stream_handler)
        loggers[name] = logger
    return loggers[name]


def debug_log():
    app_log.setLevel(logging.DEBUG)
    gen_log.setLevel(logging.DEBUG)
    access_log.setLevel(logging.DEBUG)
