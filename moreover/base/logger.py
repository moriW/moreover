#! /bin/python
# logger help
#
# @file: logger
# @time: 2022/02/01
# @author: Mori
#


import sys
import logging


def gen_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(name)s@%(asctime)s-%(levelname)s: %(message)s", "%Y/%m/%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
