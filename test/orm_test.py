#! /usr/bin/env python
#
#
# @file: web
# @time: 2022/01/28
# @author: Mori
#

import bson
import random
import asyncio
from tornado.options import options

from moreover.orm.motor import Collection


class Test(Collection):
    ...


async def test_update():
    test_instance = await Test.get_one(bson.ObjectId("61f8f2174896c8281cabdb7a"))
    test_instance.update_document(aaa="taohnuchtaoe")
    print(await test_instance.save())


async def main():
    for _ in range(20):
        test_instance = Test({"k": random.randint(1, 200)})
        await test_instance.save()
    data, count = await Test.get({})
    print(data, count)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_update())
