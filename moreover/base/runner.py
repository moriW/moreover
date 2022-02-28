#! /usr/bin/env python
# executor
#
# @file: runner
# @time: 2022/02/28
# @author: Mori
#


from typing import Awaitable, Optional
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class AsyncExecutorMeta(type):

    __executor = None

    @classmethod
    def get_executor(cls) -> ThreadPoolExecutor:
        if cls.__executor is None:
            cls.__executor = ThreadPoolExecutor(10)
        return cls.__executor

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        new_cls.executor = cls.get_executor()
        return new_cls


class AsyncExecutor(object, metaclass=AsyncExecutorMeta):
    @classmethod
    def task(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @run_on_executor
    def executor_from_executor(cls, *args, **kwargs) -> Optional[Awaitable]:
        return cls.task(*args, **kwargs)
