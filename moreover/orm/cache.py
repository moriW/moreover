#! /bin/python
# cache use
#
# @file: cache
# @time: 2022/02/03
# @author: Mori
#

import json
import pickle
import hashlib
import inspect
import aiomcache
from functools import wraps
from typing import List, Any, Callable, Awaitable, Optional

from moreover.base.logger import gen_logger
from moreover.base.config import global_config, define

logger = gen_logger("cache")
AsyncCallable = Callable[[int], Awaitable[Optional[Any]]]

define("MEMCACHE_HOST", default_value="MEMCACHE_HOST")
define("MEMCACHE_PORT", default_value="MEMCACHE_PORT")


class AioCacher:
    memcache_client: aiomcache.Client = None

    @classmethod
    def get_client(cls) -> aiomcache.Client:
        if cls.memcache_client is None:
            cls.memcache_client = aiomcache.Client(
                global_config.MEMCACHE_HOST, global_config.MEMCACHE_PORT
            )
        return cls.memcache_client

    @classmethod
    async def memcached_set(cls, k: str, v: Any, ttl: int):
        client = cls.get_client()
        await client.set(k.encode("utf8"), pickle.dumps(v), exptime=ttl)

    @classmethod
    async def memcached_get(cls, k: str) -> Any:
        client = cls.get_client()
        data = await client.get(k.encode("utf8"))
        if data is not None:
            return pickle.loads(data)
        return None

    @classmethod
    async def memecached_clean(cls, prefix: str):
        await cls.get_client().delete((prefix + "*").encode("utf8"))


def cache_it(
    ttl: int = 30, cache_positions: List[int] = None, cache_keys: List[str] = None
):
    def wraper(func: AsyncCallable):
        @wraps(func)
        async def inner_wraper(*args, **kwargs):
            key_prefix = inspect.getmodule(func).__name__ + "_" + func.__name__
            key = ""
            key_gen_obj = {}

            if cache_positions:
                key_gen_obj["args"] = [args[x] for x in cache_positions]
            else:
                key_gen_obj["args"] = args

            if cache_keys:
                key_gen_obj["kwargs"] = {k: kwargs[k] for k in cache_keys}
            else:
                key_gen_obj["kwargs"] = kwargs

            try:
                key = key_prefix + (
                    "_"
                    + hashlib.md5(
                        json.dumps({"args": args, "kwargs": kwargs}).encode("utf8")
                    ).hexdigest()
                )
            except Exception as e:
                logger.error(
                    f"make_key failed @ {func.__name__}, args parse failed: {e}"
                )
            cached_data = await AioCacher.memcached_get(key)
            if cached_data:
                logger.info(f"set cache for {key_prefix}")
                return cached_data
            data = await func(*args, **kwargs)
            if key:
                await AioCacher.memcached_set(key, data, ttl)
            return data

        return inner_wraper

    return wraper


async def remove_cache(func: AsyncCallable):
    await AioCacher.memecached_clean(func.__name__)
