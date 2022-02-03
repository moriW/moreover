import time
import bson
import random
from moreover.orm.cache import cache_it, remove_cache
from moreover.orm.motor import Collection
from .config import *


class Test(Collection):
    ...


@cache_it()
async def try_this():
    test_instance = Test(
        {
            "_id": bson.ObjectId("61fbea8f5a06e2e66756a9f8"),
            "test": random.randint(1, 100),
            "utime": time.time(),
        }
    )
    return test_instance


@cache_it()
async def save_that():
    await remove_cache(try_this)
    data = await try_this()
    await data.save()


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(save_that())
